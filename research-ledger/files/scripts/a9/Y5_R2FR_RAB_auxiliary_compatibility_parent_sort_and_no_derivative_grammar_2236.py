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
DOC = ROOT / "2236-Y5-R2FR-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_AUXILIARY_GRAMMAR_2236"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2235_doc": ROOT / "2235-Y5-R2FR-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md",
    "2235_validation": OUT / "P8_Y5_BRR545_2235_VALIDATION.csv",
    "2235_next": OUT / "P8_Y5_PARENT_QLOC_2235_NEXT_TARGET.csv",
    "2235_route": OUT / "P8_Y5_PARENT_QLOC_2235_ROUTE_DECISION_LEDGER.csv",
    "2235_boundary": OUT / "P8_Y5_PARENT_QLOC_2235_BOUNDARY_DEGREE_COUNT_GATE.csv",
    "1563_doc": ROOT / "1563-Y5-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md",
    "1563_validation": OUT / "P8_Y5_BRR545_1563_VALIDATION.csv",
    "1563_source": OUT / "P8_Y5_PARENT_QLOC_1563_SOURCE_REGISTER.csv",
    "1563_sort": OUT / "P8_Y5_PARENT_QLOC_1563_PARENT_SORT_AUDIT.csv",
    "1563_grammar": OUT / "P8_Y5_PARENT_QLOC_1563_NO_DERIVATIVE_GRAMMAR_GATE.csv",
    "1563_elimination": OUT / "P8_Y5_PARENT_QLOC_1563_AUXILIARY_ELIMINATION_GATE.csv",
    "1563_fallback": OUT / "P8_Y5_PARENT_QLOC_1563_FINITE_ZR_QR_FALLBACK_LEDGER.csv",
    "1563_runner": OUT / "P8_Y5_PARENT_QLOC_1563_RUNNER_NONCLAIM.csv",
    "1563_claim": OUT / "P8_Y5_PARENT_QLOC_1563_CLAIM_GATE.csv",
    "1563_decision": OUT / "P8_Y5_PARENT_QLOC_1563_DECISION.csv",
    "1563_next": OUT / "P8_Y5_PARENT_QLOC_1563_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2236_SOURCE_REGISTER.csv"
PARENT_SORT = OUT / "P8_Y5_PARENT_QLOC_2236_PARENT_SORT_AUDIT.csv"
NO_DERIVATIVE = OUT / "P8_Y5_PARENT_QLOC_2236_NO_DERIVATIVE_GRAMMAR_GATE.csv"
AUXILIARY_ELIMINATION = OUT / "P8_Y5_PARENT_QLOC_2236_AUXILIARY_ELIMINATION_GATE.csv"
FINITE_FALLBACK = OUT / "P8_Y5_PARENT_QLOC_2236_FINITE_ZR_QR_FALLBACK_LEDGER.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_2236_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2236_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2236_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2236_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2236_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2236_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2236_RAB_AUXILIARY_GRAMMAR_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_auxiliary_grammar_nonclaim_2236.csv",
    "beta_docs": BETA_DOCS / "RAB_AUXILIARY_GRAMMAR_2236_NONCLAIM.csv",
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
        "scripts/Y5_RAB_auxiliary_compatibility_parent_sort_and_no_derivative_grammar.py",
        "scripts/Y5_R2FR_RAB_auxiliary_compatibility_parent_sort_and_no_derivative_grammar_2236.py",
    ),
    (
        "scripts/Y5_RAB_vertical_null_presymplectic_degeneracy_or_finite_ZR_intake.py",
        "scripts/Y5_R2FR_RAB_vertical_null_presymplectic_degeneracy_or_finite_ZR_intake_2237.py",
    ),
    (
        "NEXT_1564_VERTICAL_NULL_PRESYMPLECTIC_DEGENERACY_OR_FINITE_ZR_INTAKE",
        "NEXT_2237_VERTICAL_NULL_PRESYMPLECTIC_DEGENERACY_OR_FINITE_ZR_INTAKE",
    ),
    ("NEXT_1564", "NEXT_2237"),
    ("1564", "2237"),
    ("1563", "2236"),
    ("1562", "2235"),
    ("1561", "2234"),
    ("1560", "2233"),
    ("1559", "2232"),
]


GENERATED = [
    SOURCE_REGISTER,
    PARENT_SORT,
    NO_DERIVATIVE,
    AUXILIARY_ELIMINATION,
    FINITE_FALLBACK,
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


def formalization_2236_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2236" in path.name
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
        role = "current R2FR lambda_R handoff" if key.startswith("2235") else "older R_AB auxiliary grammar evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2236_{index}_{key}",
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


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target in COPY_TARGETS.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FINITE_FALLBACK, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(FINITE_FALLBACK),
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
    parent_sort: list[dict[str, Any]],
    no_derivative: list[dict[str, Any]],
    auxiliary: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2236 - Y5/R2FR R_AB Auxiliary Compatibility Parent Sort and No-Derivative Grammar",
            "## Verdict\n"
            "- 2236 imports the old `1563` auxiliary-compatibility grammar gate into the current R2FR chain after `2235` selected this route.\n"
            "- The algebraic elimination route is still the best non-cheaty local-GR path, but only as an exact conditional.\n"
            "- To upgrade it into a theorem, `R_AB` must be parent-typed as an auxiliary/vertical compatibility coordinate rather than an observable physical scalar/tensor.\n"
            "- The parent grammar must forbid `D R_AB`, `D Lambda_R`, vertical metrics/connections, and boundary derivative terms; current sources do not parent-sign those bans.\n"
            "- Therefore `Z_R=0`, `q_R=0`, and local GR/Newton recovery remain nonclaim.\n"
            "- If the vertical-null proof fails, the finite `Z_R/q_R` residual branch becomes mandatory rather than optional.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Parent Sort Audit\n"
            + md_table(parent_sort, ["sort_id", "parent_sort_statement", "claim_effect_if_signed", "status", "blocker"]),
            "## No-Derivative Grammar Gate\n"
            + md_table(no_derivative, ["grammar_id", "grammar_clause", "why_needed", "status", "blocker_or_effect"]),
            "## Auxiliary Elimination Gate\n"
            + md_table(auxiliary, ["elimination_id", "variation_or_step", "result", "status", "blocker"]),
            "## Finite Z_R/q_R Fallback Ledger\n"
            + md_table(fallback, ["fallback_id", "coefficient", "meaning", "required_input", "status", "template_paths"]),
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
            "This checkpoint answers the important question cleanly: the auxiliary route is not nonsense, but it needs a parent object-language theorem. We cannot just ban derivatives by taste. The next proof target is therefore vertical-null presymplectic degeneracy: if `R_AB` lives in a null fibre with no vertical metric or connection, the derivative terms are genuinely illegal. If not, we accept a finite residual branch and test it.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    parent_sort = read_csv(PARENT_SORT)
    no_derivative = read_csv(NO_DERIVATIVE)
    auxiliary = read_csv(AUXILIARY_ELIMINATION)
    fallback = read_csv(FINITE_FALLBACK)
    runner = read_csv(RUNNER)
    claim = read_csv(CLAIM_GATE)
    decision = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) and source_register_paths_exist() else "FAIL",
            "detail": "all direct and registered 2236 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2235_validation"]) and validation_pass(SOURCE_FILES["1563_validation"]) else "FAIL",
            "detail": "2235 and 1563 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_02_sort_countermodel",
            "result": "PASS" if any(row.get("status") == "LEGAL_COUNTERMODEL" for row in parent_sort) else "FAIL",
            "detail": "physical R_AB countermodel recorded",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_03_sort_not_signed",
            "result": "PASS" if any("NOT_PARENT" in row.get("status", "") or row.get("status") == "CANDIDATE_ONLY" for row in parent_sort) else "FAIL",
            "detail": "auxiliary/vertical representative sort remains conditional",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_04_grammar_fails",
            "result": "PASS" if any(row.get("status") == "FAIL_CURRENT_THEOREM" for row in no_derivative) else "FAIL",
            "detail": "no-derivative grammar fails current theorem claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_05_elimination_conditional",
            "result": "PASS" if any(row.get("status") == "EXACT_CONDITIONAL" for row in auxiliary) and any(row.get("status") == "BLOCKED_NO_CLAIM" for row in auxiliary) else "FAIL",
            "detail": "Lambda_R/R_AB elimination recorded as exact conditional but not claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_06_fallback_inputs_missing",
            "result": "PASS"
            if fallback
            and all(row.get("status") in {"MISSING_SOURCE_BACKED_INPUT", "NONCLAIM_TEMPLATE_ONLY"} for row in fallback)
            and any(row.get("status") == "MISSING_SOURCE_BACKED_INPUT" for row in fallback)
            else "FAIL",
            "detail": "finite Z_R/q_R fallback retained with missing sourced inputs",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_07_runner_fallback",
            "result": "PASS" if any(row.get("current_status") == "RETAIN_NONCLAIM_FALLBACK" for row in runner) else "FAIL",
            "detail": "runner retains finite residual fallback",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_08_claim_gates",
            "result": "PASS" if all("BLOCKED" in row.get("status", "") or row.get("status", "").startswith("PASS") for row in claim) else "FAIL",
            "detail": "all claim gates remain blocked/nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_09_source_path_fields",
            "result": "PASS"
            if delimited_paths_exist([PARENT_SORT, NO_DERIVATIVE, AUXILIARY_ELIMINATION, CLAIM_GATE], ["source_paths"])
            and delimited_paths_exist([FINITE_FALLBACK], ["template_paths"])
            else "FAIL",
            "detail": "all source/template path fields resolve locally",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_10_decision_next",
            "result": "PASS"
            if any(row.get("result") == "NEXT_2237_VERTICAL_NULL_PRESYMPLECTIC_DEGENERACY_OR_FINITE_ZR_INTAKE" for row in decision)
            else "FAIL",
            "detail": "decision selects vertical-null presymplectic degeneracy or finite Z_R intake next",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_11_next_target",
            "result": "PASS" if next_target[0]["next_target"].startswith("2237-Y5-R2FR-RAB-vertical-null-presymplectic") else "FAIL",
            "detail": "next target is current-numbered vertical-null/fallback-intake gate",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_12_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2236 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_13_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated prediction/claim flags remain false",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_14_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch/quarantine nonclaim copies written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_15_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_16_formalization_no_2236",
            "result": "PASS" if formalization_2236_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2236 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_17_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2236 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2236_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2236 keeps R_AB auxiliary grammar exact conditional, retains finite Z_R/q_R fallback, and selects vertical-null proof or finite intake next",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    parent_sort = transform_old_csv(SOURCE_FILES["1563_sort"])
    no_derivative = transform_old_csv(SOURCE_FILES["1563_grammar"])
    auxiliary = transform_old_csv(SOURCE_FILES["1563_elimination"])
    fallback = transform_old_csv(SOURCE_FILES["1563_fallback"])
    runner = transform_old_csv(SOURCE_FILES["1563_runner"])
    claim = transform_old_csv(SOURCE_FILES["1563_claim"])
    decision = transform_old_csv(SOURCE_FILES["1563_decision"])
    next_target = transform_old_csv(SOURCE_FILES["1563_next"])

    write_csv(SOURCE_REGISTER, source)
    write_csv(PARENT_SORT, parent_sort)
    write_csv(NO_DERIVATIVE, no_derivative)
    write_csv(AUXILIARY_ELIMINATION, auxiliary)
    write_csv(FINITE_FALLBACK, fallback)
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
            parent_sort,
            no_derivative,
            auxiliary,
            fallback,
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
        raise SystemExit(f"2236 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
