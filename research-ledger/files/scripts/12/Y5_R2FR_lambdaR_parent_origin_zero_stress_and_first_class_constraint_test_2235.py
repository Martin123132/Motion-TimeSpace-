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
DOC = ROOT / "2235-Y5-R2FR-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_LAMBDAR_ORIGIN_ZERO_STRESS_2235"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2234_doc": ROOT / "2234-Y5-R2FR-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
    "2234_validation": OUT / "P8_Y5_BRR545_2234_VALIDATION.csv",
    "2234_next": OUT / "P8_Y5_PARENT_QLOC_2234_NEXT_TARGET.csv",
    "2234_euler": OUT / "P8_Y5_PARENT_QLOC_2234_EULER_VARIATION_GATE.csv",
    "2234_ansatz": OUT / "P8_Y5_PARENT_QLOC_2234_MINIMAL_ACTION_ANSATZ_REGISTER.csv",
    "1562_doc": ROOT / "1562-Y5-lambdaR-parent-origin-zero-stress-and-first-class-constraint-test.md",
    "1562_validation": OUT / "P8_Y5_BRR545_1562_VALIDATION.csv",
    "1562_source": OUT / "P8_Y5_PARENT_QLOC_1562_SOURCE_REGISTER.csv",
    "1562_origin": OUT / "P8_Y5_PARENT_QLOC_1562_LAMBDAR_ORIGIN_AUDIT.csv",
    "1562_stress": OUT / "P8_Y5_PARENT_QLOC_1562_ZERO_STRESS_VARIATION_GATE.csv",
    "1562_class": OUT / "P8_Y5_PARENT_QLOC_1562_CONSTRAINT_CLASS_GATE.csv",
    "1562_boundary": OUT / "P8_Y5_PARENT_QLOC_1562_BOUNDARY_DEGREE_COUNT_GATE.csv",
    "1562_route": OUT / "P8_Y5_PARENT_QLOC_1562_ROUTE_DECISION_LEDGER.csv",
    "1562_runner": OUT / "P8_Y5_PARENT_QLOC_1562_RUNNER_NONCLAIM.csv",
    "1562_claim": OUT / "P8_Y5_PARENT_QLOC_1562_CLAIM_GATE.csv",
    "1562_decision": OUT / "P8_Y5_PARENT_QLOC_1562_DECISION.csv",
    "1562_next": OUT / "P8_Y5_PARENT_QLOC_1562_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2235_SOURCE_REGISTER.csv"
LAMBDAR_ORIGIN = OUT / "P8_Y5_PARENT_QLOC_2235_LAMBDAR_ORIGIN_AUDIT.csv"
ZERO_STRESS = OUT / "P8_Y5_PARENT_QLOC_2235_ZERO_STRESS_VARIATION_GATE.csv"
CONSTRAINT_CLASS = OUT / "P8_Y5_PARENT_QLOC_2235_CONSTRAINT_CLASS_GATE.csv"
BOUNDARY = OUT / "P8_Y5_PARENT_QLOC_2235_BOUNDARY_DEGREE_COUNT_GATE.csv"
ROUTE_DECISION = OUT / "P8_Y5_PARENT_QLOC_2235_ROUTE_DECISION_LEDGER.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_2235_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2235_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2235_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2235_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2235_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2235_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2235_LAMBDAR_ORIGIN_ZERO_STRESS_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "lambdaR_origin_zero_stress_nonclaim_2235.csv",
    "beta_docs": BETA_DOCS / "LAMBDAR_ORIGIN_ZERO_STRESS_2235_NONCLAIM.csv",
}


OLD_TO_NEW = [
    (
        "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
        "2234-Y5-R2FR-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
    ),
    (
        "1555-Y5-gauge-noether-zero-charge-qsector-origin-audit.md",
        "2228-Y5-R2FR-gauge-noether-zero-charge-qsector-origin-audit.md",
    ),
    (
        "1563-Y5-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md",
        "2236-Y5-R2FR-RAB-auxiliary-compatibility-parent-sort-and-no-derivative-grammar.md",
    ),
    (
        "scripts/Y5_RAB_auxiliary_compatibility_parent_sort_and_no_derivative_grammar.py",
        "scripts/Y5_R2FR_RAB_auxiliary_compatibility_parent_sort_and_no_derivative_grammar_2236.py",
    ),
    ("NEXT_1563_AUXILIARY_PARENT_SORT_NO_DERIVATIVE_GRAMMAR", "NEXT_2236_AUXILIARY_PARENT_SORT_NO_DERIVATIVE_GRAMMAR"),
    ("NEXT_1563", "NEXT_2236"),
    ("1563", "2236"),
    ("1562", "2235"),
    ("1561", "2234"),
    ("1560", "2233"),
    ("1559", "2232"),
    ("1558", "2231"),
    ("1557", "2230"),
    ("1556", "2229"),
    ("1555", "2228"),
]


GENERATED = [
    SOURCE_REGISTER,
    LAMBDAR_ORIGIN,
    ZERO_STRESS,
    CONSTRAINT_CLASS,
    BOUNDARY,
    ROUTE_DECISION,
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


def formalization_2235_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2235" in path.name
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
        role = "current R2FR action-ansatz handoff" if key.startswith("2234") else "older lambda_R origin/zero-stress evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2235_{index}_{key}",
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


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target in COPY_TARGETS.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROUTE_DECISION, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(ROUTE_DECISION),
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
    origin: list[dict[str, Any]],
    stress: list[dict[str, Any]],
    constraint_class: list[dict[str, Any]],
    boundary: list[dict[str, Any]],
    route: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2235 - Y5/R2FR lambda_R Parent-Origin, Zero-Stress, and Constraint-Class Test",
            "## Verdict\n"
            "- 2235 imports the old `1562` lambda_R hinge test into the current R2FR chain after `2234` selected the ansatz route.\n"
            "- `delta lambda_R` still formally gives `R_AB=0`, but this remains a formal multiplier fact, not a parent derivation.\n"
            "- The first-class route remains blocked: preservation, Poisson brackets, degree count, and differentiable boundary generator are not present in the current parent data.\n"
            "- The zero-stress theorem also remains unsigned: metric variation of `lambda_R R_AB` can leak an unowned stress/reaction term unless the auxiliary equation, source silence, boundary silence, and readout stability are all proved.\n"
            "- The least-cheaty route is now second-class auxiliary compatibility: treat `R_AB`/`Lambda_R` as algebraic parent compatibility variables, forbid derivative operators on them, and eliminate them without `Q_R` hair.\n"
            "- Local GR/Newton recovery is still nonclaim; the bounded finite-q_R runner remains the honest fallback.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## lambda_R Origin Audit\n"
            + md_table(origin, ["origin_id", "route", "mechanism", "status", "problem", "decision"]),
            "## Zero-Stress Variation Gate\n"
            + md_table(stress, ["stress_id", "variation", "result", "status", "reason", "next_condition"]),
            "## Constraint-Class Gate\n"
            + md_table(constraint_class, ["class_id", "constraint_test", "required_statement", "status", "blocker"]),
            "## Boundary / Degree-Count Gate\n"
            + md_table(boundary, ["boundary_id", "gate", "required_statement", "status", "blocker"]),
            "## Route Decision Ledger\n"
            + md_table(route, ["route_id", "route", "verdict", "reason", "next_action"]),
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
            "This narrows the battlefield in a good way. The first-class language is attractive but presently too expensive: it asks for a Hamiltonian, brackets, boundary charge, and degree-count proof that the corpus does not yet supply. The auxiliary route is cleaner and more engineering-like: if the parent grammar says `R_AB` is algebraic/nonpropagating, then the local zero can be derived by elimination rather than wished into place. That is the next real leap.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    origin = read_csv(LAMBDAR_ORIGIN)
    stress = read_csv(ZERO_STRESS)
    constraint_class = read_csv(CONSTRAINT_CLASS)
    boundary = read_csv(BOUNDARY)
    route = read_csv(ROUTE_DECISION)
    runner = read_csv(RUNNER)
    claim = read_csv(CLAIM_GATE)
    decision = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) and source_register_paths_exist() else "FAIL",
            "detail": "all direct and registered 2235 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2234_validation"]) and validation_pass(SOURCE_FILES["1562_validation"]) else "FAIL",
            "detail": "2234 and 1562 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_02_origin_not_signed",
            "result": "PASS" if any(row.get("decision") == "REJECT_AS_DERIVATION" for row in origin) else "FAIL",
            "detail": "bare delta-lambda route rejected as derivation",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_03_zero_stress_fail",
            "result": "PASS" if any(row.get("status") == "FAIL_CURRENT_CLAIM" for row in stress) else "FAIL",
            "detail": "zero-stress theorem remains failed for current claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_04_first_class_blocked",
            "result": "PASS" if sum(1 for row in constraint_class if row.get("status") == "BLOCKED") >= 3 else "FAIL",
            "detail": "first-class preservation/bracket/degree/boundary route remains blocked",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_05_boundary_unsigned",
            "result": "PASS" if boundary and all(row.get("status") == "UNSIGNED" for row in boundary) else "FAIL",
            "detail": "boundary, degree-count, matter, readout, and operator gates remain unsigned",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_06_best_route",
            "result": "PASS" if any(row.get("verdict") == "BEST_DERIVATION_ROUTE_CONDITIONAL" for row in route) else "FAIL",
            "detail": "second-class auxiliary compatibility route selected as least-cheaty conditional repair",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_07_runner_claim_block",
            "result": "PASS" if any(row.get("current_status") == "BLOCKED_NO_CLAIM" for row in runner) else "FAIL",
            "detail": "runner blocks local GR/Newton claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_08_claim_gates",
            "result": "PASS" if all("BLOCKED" in row.get("status", "") or row.get("status", "").startswith("PASS") for row in claim) else "FAIL",
            "detail": "all claim gates remain blocked/nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_09_table_source_paths",
            "result": "PASS" if table_source_paths_exist([LAMBDAR_ORIGIN, ZERO_STRESS, CONSTRAINT_CLASS, BOUNDARY, CLAIM_GATE]) else "FAIL",
            "detail": "all semicolon-delimited source paths in origin/stress/class/boundary/claim rows resolve locally",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_10_decision_next",
            "result": "PASS" if any(row.get("result") == "NEXT_2236_AUXILIARY_PARENT_SORT_NO_DERIVATIVE_GRAMMAR" for row in decision) else "FAIL",
            "detail": "decision selects auxiliary parent sort/no-derivative grammar next",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_11_next_target",
            "result": "PASS" if next_target[0]["next_target"].startswith("2236-Y5-R2FR-RAB-auxiliary-compatibility") else "FAIL",
            "detail": "next target is current-numbered R_AB auxiliary compatibility grammar test",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_12_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2235 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_13_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated prediction/claim flags remain false",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_14_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch/quarantine nonclaim copies written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_15_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_16_formalization_no_2235",
            "result": "PASS" if formalization_2235_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2235 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_17_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2235 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2235_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2235 rejects current lambda_R parent/zero-stress promotion, selects auxiliary compatibility grammar next, and keeps local GR nonclaim",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    origin = transform_old_csv(SOURCE_FILES["1562_origin"])
    stress = transform_old_csv(SOURCE_FILES["1562_stress"])
    constraint_class = transform_old_csv(SOURCE_FILES["1562_class"])
    boundary = transform_old_csv(SOURCE_FILES["1562_boundary"])
    route = transform_old_csv(SOURCE_FILES["1562_route"])
    runner = transform_old_csv(SOURCE_FILES["1562_runner"])
    claim = transform_old_csv(SOURCE_FILES["1562_claim"])
    decision = transform_old_csv(SOURCE_FILES["1562_decision"])
    next_target = transform_old_csv(SOURCE_FILES["1562_next"])

    write_csv(SOURCE_REGISTER, source)
    write_csv(LAMBDAR_ORIGIN, origin)
    write_csv(ZERO_STRESS, stress)
    write_csv(CONSTRAINT_CLASS, constraint_class)
    write_csv(BOUNDARY, boundary)
    write_csv(ROUTE_DECISION, route)
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
            origin,
            stress,
            constraint_class,
            boundary,
            route,
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
        raise SystemExit(f"2235 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
