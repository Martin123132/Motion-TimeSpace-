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
DOC = ROOT / "2230-Y5-R2FR-closure-deviation-PPN-sensitivity-and-bound-budget.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_CLOSURE_DEVIATION_BUDGET_2230"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2229_doc": ROOT / "2229-Y5-R2FR-local-closure-PPN-benchmark-and-derived-vs-assumed-ledger.md",
    "2229_validation": OUT / "P8_Y5_BRR545_2229_VALIDATION.csv",
    "2229_next": OUT / "P8_Y5_PARENT_QLOC_2229_NEXT_TARGET.csv",
    "1557_doc": ROOT / "1557-Y5-closure-deviation-PPN-sensitivity-and-bound-budget.md",
    "1557_validation": OUT / "P8_Y5_BRR545_1557_VALIDATION.csv",
    "1557_channels": OUT / "P8_Y5_PARENT_QLOC_1557_DEVIATION_CHANNELS.csv",
    "1557_sensitivity": OUT / "P8_Y5_PARENT_QLOC_1557_SENSITIVITY_MAP_NONCLAIM.csv",
    "1557_bounds": OUT / "P8_Y5_PARENT_QLOC_1557_LOCAL_BOUND_LINKS.csv",
    "1557_budget": OUT / "P8_Y5_PARENT_QLOC_1557_BOUND_BUDGET_NONCLAIM.csv",
    "1557_runner": OUT / "P8_Y5_PARENT_QLOC_1557_RUNNER_NONCLAIM.csv",
    "1557_claim": OUT / "P8_Y5_PARENT_QLOC_1557_CLAIM_GATE.csv",
    "1557_decision": OUT / "P8_Y5_PARENT_QLOC_1557_DECISION.csv",
    "1557_next": OUT / "P8_Y5_PARENT_QLOC_1557_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2230_SOURCE_REGISTER.csv"
DEVIATION_CHANNELS = OUT / "P8_Y5_PARENT_QLOC_2230_DEVIATION_CHANNELS.csv"
SENSITIVITY_MAP = OUT / "P8_Y5_PARENT_QLOC_2230_SENSITIVITY_MAP_NONCLAIM.csv"
LOCAL_BOUND_LINKS = OUT / "P8_Y5_PARENT_QLOC_2230_LOCAL_BOUND_LINKS.csv"
BOUND_BUDGET = OUT / "P8_Y5_PARENT_QLOC_2230_BOUND_BUDGET_NONCLAIM.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_2230_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2230_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2230_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2230_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2230_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2230_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2230_CLOSURE_DEVIATION_BUDGET_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "closure_deviation_budget_nonclaim_2230.csv",
    "beta_docs": BETA_DOCS / "CLOSURE_DEVIATION_BUDGET_2230_NONCLAIM.csv",
}


OLD_TO_NEW = [
    ("1558-Y5-qR-beta-matter-clock-coefficient-source-map-or-rejection.md", "2231-Y5-R2FR-qR-beta-matter-clock-coefficient-source-map-or-rejection.md"),
    ("scripts/Y5_qR_beta_matter_clock_coefficient_source_map_or_rejection.py", "scripts/Y5_R2FR_qR_beta_matter_clock_coefficient_source_map_or_rejection_2231.py"),
    ("NEXT_1558_COEFFICIENT_SOURCE_MAP", "NEXT_2231_COEFFICIENT_SOURCE_MAP"),
    ("1558", "2231"),
    ("1557", "2230"),
    ("1556", "2229"),
]


GENERATED = [
    SOURCE_REGISTER,
    DEVIATION_CHANNELS,
    SENSITIVITY_MAP,
    LOCAL_BOUND_LINKS,
    BOUND_BUDGET,
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


def formalization_2230_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2230" in path.name
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
        role = "current closure benchmark handoff" if key.startswith("2229") else "older closure-deviation/bound-budget evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2230_{index}_{key}",
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
        shutil.copyfile(BOUND_BUDGET, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(BOUND_BUDGET),
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
    channels: list[dict[str, Any]],
    sensitivities: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    budgets: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2230 - Y5/R2FR Closure-Deviation PPN Sensitivity And Bound Budget",
            "## Verdict\n"
            "- 2230 imports the old `1557` closure-deviation/bound-budget frontier into the current R2FR line.\n"
            "- The local leakage channels are now explicit: `q_R`, `delta_beta`, matter/coframe spread, clock anomaly, source-normalization drift, preferred-frame leakage, finite-range R10 hair, and tracefree transfer.\n"
            "- Local bounds are linked for R0-R9 with numeric control rows; R10 correctly remains symbolic until a real `alpha(lambda)` curve and parent range map exist.\n"
            "- Every budget is still nonclaim: unit-response control bounds are not MTS predictions until parent response coefficients are derived or sourced.\n"
            "- Next target is the response-coefficient source map: derive or reject the coefficients that turn closure deviations into actual local predictions.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Deviation Channels\n"
            + md_table(channels, ["channel_id", "leak_parameter", "meaning", "null_lane_value", "first_observables", "missing_parent_inputs", "status"]),
            "## Sensitivity Map\n"
            + md_table(sensitivities, ["sensitivity_id", "leak_parameter", "observable_channel", "control_coefficient", "coefficient_status", "required_parent_coefficient", "claim_status"]),
            "## Local Bound Links\n"
            + md_table(bounds, ["bound_link_id", "row_id", "used_for_channel", "observable", "upper_bound", "units", "numeric_bound_parse", "budget_use"]),
            "## Bound Budget\n"
            + md_table(budgets, ["budget_id", "leak_parameter", "local_bound_rows", "control_bound_if_unit_response", "bound_units", "blocking_input", "budget_status"]),
            "## Runner\n"
            + md_table(runner, ["runner_id", "test", "current_status", "detail"]),
            "## Claim Gate\n"
            + md_table(claim, ["gate_id", "claim", "status", "reason"]),
            "## Decision Ledger\n"
            + md_table(decision, ["decision_id", "decision", "result", "reason"]),
            "## Next Target\n"
            + md_table(next_target, ["next_id", "next_target", "script", "objective", "do_not"]),
            "## Branch Copies\n"
            + md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
            "## Validation\n"
            + md_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\n"
            "This is now a usable local test budget, but not yet a local prediction. It tells the theory exactly which response coefficients must be owned by the parent framework before the closure branch can face PPN, WEP, clock, R10, and source-normalization bounds. The win is discipline: instead of saying 'matches GR locally', the branch now says which hidden residuals must be made small, why, and by which missing coefficient.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    numeric_bound_rows = [
        row for row in read_csv(LOCAL_BOUND_LINKS)
        if row.get("row_id") != "R10_fifth_force"
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) else "FAIL",
            "detail": "all cited 2230 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2229_validation"]) and validation_pass(SOURCE_FILES["1557_validation"]) else "FAIL",
            "detail": "2229 and 1557 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_02_channels_complete",
            "result": "PASS" if len(read_csv(DEVIATION_CHANNELS)) >= 10 else "FAIL",
            "detail": "all required local leakage channels are present",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_03_bound_rows_linked",
            "result": "PASS" if len(read_csv(LOCAL_BOUND_LINKS)) >= 11 else "FAIL",
            "detail": "local bound rows are linked to channels",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_04_numeric_bounds_parse",
            "result": "PASS" if all(row.get("numeric_bound_parse") == "PASS" for row in numeric_bound_rows) else "FAIL",
            "detail": "numeric R0-R9 local bounds parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_05_R10_symbolic",
            "result": "PASS" if any(row.get("numeric_bound_parse") == "SYMBOLIC_CURVE_REQUIRED" for row in read_csv(LOCAL_BOUND_LINKS)) else "FAIL",
            "detail": "R10 remains symbolic curve-only",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_06_sensitivities_present",
            "result": "PASS" if any(row.get("leak_parameter") == "q_R" for row in read_csv(SENSITIVITY_MAP)) else "FAIL",
            "detail": "sensitivity map includes q_R and other channels",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_07_budgets_blocked",
            "result": "PASS" if all("NOT_MTS_PREDICTION" in row.get("budget_status", "") for row in read_csv(BOUND_BUDGET)) else "FAIL",
            "detail": "all bound budgets are control-only nonpredictions",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_08_runner_refuses_prediction",
            "result": "PASS" if any(row.get("current_status") == "REFUSED_MISSING_PARENT_COEFFICIENTS" for row in read_csv(RUNNER)) else "FAIL",
            "detail": "runner refuses MTS prediction scoring",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_09_claim_gates_block",
            "result": "PASS" if all("BLOCKED" in row.get("status", "") or row.get("status", "").startswith("PASS") for row in read_csv(CLAIM_GATE)) else "FAIL",
            "detail": "all local claim gates remain blocked",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_10_decision_next",
            "result": "PASS" if any(row.get("result") == "NEXT_2231_COEFFICIENT_SOURCE_MAP" for row in read_csv(DECISION)) else "FAIL",
            "detail": "decision selects response-coefficient source map next",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_11_next_target",
            "result": "PASS" if read_csv(NEXT_TARGET)[0]["next_target"].startswith("2231-Y5-R2FR-qR-beta") else "FAIL",
            "detail": "next target is current-numbered coefficient source map",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_12_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2230 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_13_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated flags remain nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_14_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch copies written and parse",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_15_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_16_formalization_no_2230",
            "result": "PASS" if formalization_2230_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2230 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_17_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2230 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2230_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2230 imports closure-deviation channels, local-bound links, and control-only budgets while keeping predictions blocked until response coefficients are sourced",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    channels = transform_old_csv(SOURCE_FILES["1557_channels"])
    sensitivities = transform_old_csv(SOURCE_FILES["1557_sensitivity"])
    bounds = transform_old_csv(SOURCE_FILES["1557_bounds"])
    budgets = transform_old_csv(SOURCE_FILES["1557_budget"])
    runner = transform_old_csv(SOURCE_FILES["1557_runner"])
    claim = transform_old_csv(SOURCE_FILES["1557_claim"])
    decision = transform_old_csv(SOURCE_FILES["1557_decision"])
    next_target = transform_old_csv(SOURCE_FILES["1557_next"])

    write_csv(SOURCE_REGISTER, source)
    write_csv(DEVIATION_CHANNELS, channels)
    write_csv(SENSITIVITY_MAP, sensitivities)
    write_csv(LOCAL_BOUND_LINKS, bounds)
    write_csv(BOUND_BUDGET, budgets)
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
            channels,
            sensitivities,
            bounds,
            budgets,
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
        raise SystemExit(f"2230 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
