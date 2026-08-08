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
DOC = ROOT / "2237-Y5-R2FR-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_VERTICAL_NULL_OR_ZR_INTAKE_2237"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2236_doc": ROOT / "2236-Y5-R2FR-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md",
    "2236_validation": OUT / "P8_Y5_BRR545_2236_VALIDATION.csv",
    "2236_next": OUT / "P8_Y5_PARENT_QLOC_2236_NEXT_TARGET.csv",
    "2236_sort": OUT / "P8_Y5_PARENT_QLOC_2236_PARENT_SORT_AUDIT.csv",
    "2236_fallback": OUT / "P8_Y5_PARENT_QLOC_2236_FINITE_ZR_QR_FALLBACK_LEDGER.csv",
    "1564_doc": ROOT / "1564-Y5-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md",
    "1564_validation": OUT / "P8_Y5_BRR545_1564_VALIDATION.csv",
    "1564_source": OUT / "P8_Y5_PARENT_QLOC_1564_SOURCE_REGISTER.csv",
    "1564_null": OUT / "P8_Y5_PARENT_QLOC_1564_PRESYMPLECTIC_NULL_CHAIN.csv",
    "1564_kinetic": OUT / "P8_Y5_PARENT_QLOC_1564_KINETIC_TERM_CONTRADICTION.csv",
    "1564_blockers": OUT / "P8_Y5_PARENT_QLOC_1564_PARENT_INPUT_BLOCKERS.csv",
    "1564_intake": OUT / "P8_Y5_PARENT_QLOC_1564_FINITE_ZR_INTAKE_STATUS.csv",
    "1564_runner": OUT / "P8_Y5_PARENT_QLOC_1564_RUNNER_NONCLAIM.csv",
    "1564_claim": OUT / "P8_Y5_PARENT_QLOC_1564_CLAIM_GATE.csv",
    "1564_decision": OUT / "P8_Y5_PARENT_QLOC_1564_DECISION.csv",
    "1564_next": OUT / "P8_Y5_PARENT_QLOC_1564_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2237_SOURCE_REGISTER.csv"
PRESYMPLECTIC_NULL = OUT / "P8_Y5_PARENT_QLOC_2237_PRESYMPLECTIC_NULL_CHAIN.csv"
KINETIC = OUT / "P8_Y5_PARENT_QLOC_2237_KINETIC_TERM_CONTRADICTION.csv"
BLOCKERS = OUT / "P8_Y5_PARENT_QLOC_2237_PARENT_INPUT_BLOCKERS.csv"
FINITE_INTAKE = OUT / "P8_Y5_PARENT_QLOC_2237_FINITE_ZR_INTAKE_STATUS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_2237_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2237_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2237_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2237_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2237_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2237_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2237_VERTICAL_NULL_OR_ZR_INTAKE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "vertical_null_or_ZR_intake_nonclaim_2237.csv",
    "beta_docs": BETA_DOCS / "VERTICAL_NULL_OR_ZR_INTAKE_2237_NONCLAIM.csv",
}


OLD_TO_NEW = [
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
        "scripts/Y5_RAB_vertical_null_presymplectic_degeneracy_or_finite_ZR_intake.py",
        "scripts/Y5_R2FR_RAB_vertical_null_presymplectic_degeneracy_or_finite_ZR_intake_2237.py",
    ),
    (
        "scripts/Y5_RAB_parent_theta_Omega_vR_fill_or_finite_ZR_source_row.py",
        "scripts/Y5_R2FR_RAB_parent_theta_Omega_vR_fill_or_finite_ZR_source_row_2238.py",
    ),
    (
        "NEXT_1565_PARENT_THETA_OMEGA_VR_FILL_OR_ZR_SOURCE_ROW",
        "NEXT_2238_PARENT_THETA_OMEGA_VR_FILL_OR_ZR_SOURCE_ROW",
    ),
    ("NEXT_1565", "NEXT_2238"),
    ("1565", "2238"),
    ("1564", "2237"),
    ("1563", "2236"),
    ("1562", "2235"),
    ("1561", "2234"),
]


GENERATED = [
    SOURCE_REGISTER,
    PRESYMPLECTIC_NULL,
    KINETIC,
    BLOCKERS,
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


def formalization_2237_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2237" in path.name
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
        role = "current R2FR auxiliary grammar handoff" if key.startswith("2236") else "older vertical-null/fallback evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2237_{index}_{key}",
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


def intake_folders_exist() -> bool:
    return all(resolve_project_path(row["folder"]).exists() for row in read_csv(FINITE_INTAKE))


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target in COPY_TARGETS.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FINITE_INTAKE, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(FINITE_INTAKE),
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
    null_chain: list[dict[str, Any]],
    kinetic: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
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
            "# 2237 - Y5/R2FR R_AB Vertical-Null Presymplectic Degeneracy or Finite Z_R Intake",
            "## Verdict\n"
            "- 2237 imports the old `1564` vertical-null/fallback checkpoint into the current R2FR chain after `2236` showed the auxiliary grammar is conditional.\n"
            "- There is a real conditional theorem shape: if `R_AB` is a parent presymplectic-null vertical representative with no boundary charge, then nonzero `Z_R |D R_AB|^2` contradicts that nullness.\n"
            "- This is not yet a local-GR derivation because the current corpus lacks parent `L/theta/Omega`, field-by-field `v_R`, no-vertical-metric, boundary-zero, and readout-stability proofs.\n"
            "- Finite `Z_R/q_R` intake is still nonclaim: only templates/docs exist, with no accepted source-backed rows.\n"
            "- The next target is now explicit: either instantiate parent `theta/Omega` and `v_R`, or stage strict finite `Z_R` source rows without scoring placeholders.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Presymplectic Null Chain\n"
            + md_table(null_chain, ["chain_id", "claim_piece", "mathematical_form", "status", "blocker"]),
            "## Kinetic Term Contradiction\n"
            + md_table(kinetic, ["kinetic_id", "assumption_or_operator", "calculation", "status", "meaning"]),
            "## Parent Input Blockers\n"
            + md_table(blockers, ["blocker_id", "needed_object", "why_needed", "current_status"]),
            "## Finite Z_R Intake Status\n"
            + md_table(intake, ["intake_id", "folder", "rows_found", "status", "required_before_scoring"]),
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
            "This is the best kind of partial win: not a claim, but a sharp theorem contract. We now know exactly what would make `Z_R=0` non-ad hoc: a parent presymplectic-null certificate for the `R_AB` direction. If that certificate cannot be filled, the honest route is finite residual intake and empirical bounding. No magic plateau, no vibes-based derivative ban.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    null_chain = read_csv(PRESYMPLECTIC_NULL)
    kinetic = read_csv(KINETIC)
    blockers = read_csv(BLOCKERS)
    intake = read_csv(FINITE_INTAKE)
    runner = read_csv(RUNNER)
    claim = read_csv(CLAIM_GATE)
    decision = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) and source_register_paths_exist() else "FAIL",
            "detail": "all direct and registered 2237 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2236_validation"]) and validation_pass(SOURCE_FILES["1564_validation"]) else "FAIL",
            "detail": "2236 and 1564 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_02_null_conditional",
            "result": "PASS" if any(row.get("status") == "CONDITIONAL_CONTRADICTION_WRITTEN_NOT_PARENT_PROVED" for row in null_chain) else "FAIL",
            "detail": "presymplectic null chain verdict is conditional not proved",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_03_kinetic_contradiction",
            "result": "PASS" if any(row.get("status") == "EXACT_CONDITIONAL_ON_TRUE_NULLNESS" for row in kinetic) else "FAIL",
            "detail": "kinetic contradiction is exact conditional",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_04_blockers",
            "result": "PASS" if len(blockers) >= 5 and all(row.get("current_status", "").startswith("MISSING_") for row in blockers) else "FAIL",
            "detail": "parent input blockers are recorded",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_05_intake_not_scoreable",
            "result": "PASS" if any(row.get("status") == "NO_ACCEPTED_ROWS" for row in intake) else "FAIL",
            "detail": "finite intake has no accepted source rows",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_06_runner_parent_fail",
            "result": "PASS" if any(row.get("current_status") == "FAILED_CURRENT_PARENT_PROOF" for row in runner) else "FAIL",
            "detail": "runner refuses parent-null proof",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_07_claim_gates",
            "result": "PASS" if all("BLOCKED" in row.get("status", "") or row.get("status", "").startswith("PASS") for row in claim) else "FAIL",
            "detail": "all claim gates remain blocked/nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_08_path_fields",
            "result": "PASS"
            if delimited_paths_exist([PRESYMPLECTIC_NULL, KINETIC, BLOCKERS, CLAIM_GATE], ["source_paths"]) and intake_folders_exist()
            else "FAIL",
            "detail": "source path fields and finite-intake folders resolve locally",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_09_decision_next",
            "result": "PASS" if any(row.get("result") == "NEXT_2238_PARENT_THETA_OMEGA_VR_FILL_OR_ZR_SOURCE_ROW" for row in decision) else "FAIL",
            "detail": "decision selects parent theta/Omega/vR fill or finite Z_R source row next",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_10_next_target",
            "result": "PASS" if next_target[0]["next_target"].startswith("2238-Y5-R2FR-RAB-parent-theta-Omega-vR") else "FAIL",
            "detail": "next target is current-numbered theta/Omega/vR fill or finite Z_R source row",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_11_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2237 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_12_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated prediction/claim flags remain false",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_13_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch/quarantine nonclaim copies written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_14_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_15_formalization_no_2237",
            "result": "PASS" if formalization_2237_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2237 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_16_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2237 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2237_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2237 preserves exact conditional vertical-null contradiction, refuses local claim, and selects theta/Omega/vR fill or finite Z_R source intake next",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    null_chain = transform_old_csv(SOURCE_FILES["1564_null"])
    kinetic = transform_old_csv(SOURCE_FILES["1564_kinetic"])
    blockers = transform_old_csv(SOURCE_FILES["1564_blockers"])
    intake = transform_old_csv(SOURCE_FILES["1564_intake"])
    runner = transform_old_csv(SOURCE_FILES["1564_runner"])
    claim = transform_old_csv(SOURCE_FILES["1564_claim"])
    decision = transform_old_csv(SOURCE_FILES["1564_decision"])
    next_target = transform_old_csv(SOURCE_FILES["1564_next"])

    write_csv(SOURCE_REGISTER, source)
    write_csv(PRESYMPLECTIC_NULL, null_chain)
    write_csv(KINETIC, kinetic)
    write_csv(BLOCKERS, blockers)
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
            null_chain,
            kinetic,
            blockers,
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
        raise SystemExit(f"2237 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
