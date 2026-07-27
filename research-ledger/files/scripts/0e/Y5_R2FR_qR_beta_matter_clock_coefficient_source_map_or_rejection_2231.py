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
DOC = ROOT / "2231-Y5-R2FR-qR-beta-matter-clock-coefficient-source-map-or-rejection.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_COEFFICIENT_SOURCE_MAP_2231"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2230_doc": ROOT / "2230-Y5-R2FR-closure-deviation-PPN-sensitivity-and-bound-budget.md",
    "2230_validation": OUT / "P8_Y5_BRR545_2230_VALIDATION.csv",
    "2230_next": OUT / "P8_Y5_PARENT_QLOC_2230_NEXT_TARGET.csv",
    "1558_doc": ROOT / "1558-Y5-qR-beta-matter-clock-coefficient-source-map-or-rejection.md",
    "1558_validation": OUT / "P8_Y5_BRR545_1558_VALIDATION.csv",
    "1558_ppn_coefficients": OUT / "P8_Y5_PARENT_QLOC_1558_PPN_COEFFICIENT_DERIVATION.csv",
    "1558_phenomenology": OUT / "P8_Y5_PARENT_QLOC_1558_PHENOMENOLOGICAL_COEFFICIENT_MAP.csv",
    "1558_readiness": OUT / "P8_Y5_PARENT_QLOC_1558_COEFFICIENT_READINESS_MATRIX.csv",
    "1558_rejections": OUT / "P8_Y5_PARENT_QLOC_1558_COEFFICIENT_REJECTION_LEDGER.csv",
    "1558_runner": OUT / "P8_Y5_PARENT_QLOC_1558_RUNNER_NONCLAIM.csv",
    "1558_claim": OUT / "P8_Y5_PARENT_QLOC_1558_CLAIM_GATE.csv",
    "1558_decision": OUT / "P8_Y5_PARENT_QLOC_1558_DECISION.csv",
    "1558_next": OUT / "P8_Y5_PARENT_QLOC_1558_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2231_SOURCE_REGISTER.csv"
PPN_COEFFICIENTS = OUT / "P8_Y5_PARENT_QLOC_2231_PPN_COEFFICIENT_DERIVATION.csv"
PHENOMENOLOGY = OUT / "P8_Y5_PARENT_QLOC_2231_PHENOMENOLOGICAL_COEFFICIENT_MAP.csv"
READINESS = OUT / "P8_Y5_PARENT_QLOC_2231_COEFFICIENT_READINESS_MATRIX.csv"
REJECTIONS = OUT / "P8_Y5_PARENT_QLOC_2231_COEFFICIENT_REJECTION_LEDGER.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_2231_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2231_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2231_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2231_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2231_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2231_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2231_COEFFICIENT_SOURCE_MAP_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "coefficient_source_map_nonclaim_2231.csv",
    "beta_docs": BETA_DOCS / "COEFFICIENT_SOURCE_MAP_2231_NONCLAIM.csv",
}


OLD_TO_NEW = [
    ("1559-Y5-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt.md", "2232-Y5-R2FR-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt.md"),
    ("scripts/Y5_qR_delta_beta_two_parameter_PPN_control_runner_and_zero_condition_hunt.py", "scripts/Y5_R2FR_qR_delta_beta_two_parameter_PPN_control_runner_and_zero_condition_hunt_2232.py"),
    ("NEXT_1559_TWO_PARAMETER_PPN_CONTROL_RUNNER_AND_ZERO_CONDITION_HUNT", "NEXT_2232_TWO_PARAMETER_PPN_CONTROL_RUNNER_AND_ZERO_CONDITION_HUNT"),
    ("NEXT_1559", "NEXT_2232"),
    ("1559", "2232"),
    ("1558", "2231"),
    ("1557", "2230"),
    ("1556", "2229"),
]


GENERATED = [
    SOURCE_REGISTER,
    PPN_COEFFICIENTS,
    PHENOMENOLOGY,
    READINESS,
    REJECTIONS,
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


def formalization_2231_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2231" in path.name
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
        role = "current deviation-budget handoff" if key.startswith("2230") else "older coefficient source-map evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2231_{index}_{key}",
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
        shutil.copyfile(READINESS, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(READINESS),
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
    ppn: list[dict[str, Any]],
    phen: list[dict[str, Any]],
    readiness: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2231 - Y5/R2FR q_R Beta Matter Clock Coefficient Source Map Or Rejection",
            "## Verdict\n"
            "- 2231 imports the old `1558` coefficient source-map frontier into the current R2FR line.\n"
            "- The useful win is the PPN dictionary: `q_R` maps to `gamma-1`, light bending and Shapiro residuals carry the GR/2 coefficient, and perihelion carries the `(2 q_R - delta_beta)/3` structure.\n"
            "- `delta_beta` is defined as `beta-1`, but the parent theory still has to supply the nonlinear completion that predicts or zeros it.\n"
            "- Clock and WEP/matter rows are usable as phenomenological proxy parameters only; source normalization, preferred-frame, flux, R10, and tracefree response coefficients remain rejected for scoring.\n"
            "- Local-bound scoring remains blocked until the parent action predicts the leak parameters or proves their zero conditions.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## PPN Coefficient Derivation\n"
            + md_table(ppn, ["coefficient_id", "leak_parameter", "observable_response", "coefficient_value", "coefficient_units", "coefficient_status", "translation_ready", "parent_prediction_ready"]),
            "## Phenomenological Coefficient Map\n"
            + md_table(phen, ["phenomenology_id", "leak_parameter", "observable_response", "coefficient_value", "coefficient_status", "translation_ready", "parent_prediction_ready"]),
            "## Readiness Matrix\n"
            + md_table(readiness, ["readiness_id", "leak_parameter", "observable_response", "translation_ready", "parent_prediction_ready", "score_ready", "status"]),
            "## Rejection Ledger\n"
            + md_table(rejections, ["rejection_id", "leak_parameter", "observable_response", "missing_input", "reentry_condition", "status"]),
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
            "This checkpoint separates a real mathematical translation from a physical prediction. The local branch can now translate `q_R` and `delta_beta` into standard PPN residuals cleanly, which is progress. But MTS has not yet earned a local-GR claim because the parent theory must still set `q_R=0`, set `delta_beta=0`, or predict small nonzero values from field equations rather than from local-bound fitting.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    ppn = read_csv(PPN_COEFFICIENTS)
    readiness = read_csv(READINESS)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) else "FAIL",
            "detail": "all cited 2231 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2230_validation"]) and validation_pass(SOURCE_FILES["1558_validation"]) else "FAIL",
            "detail": "2230 and 1558 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_02_qR_gamma",
            "result": "PASS" if any(row["leak_parameter"] == "q_R" and row["observable_response"] == "gamma_minus_1" and row["coefficient_value"] == "1" for row in ppn) else "FAIL",
            "detail": "q_R to gamma-minus-one coefficient derived",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_03_light_shapiro_coefficients",
            "result": "PASS" if any(row["observable_response"] == "solar_light_bending_residual" for row in ppn) and any(row["observable_response"] == "solar_Shapiro_residual" for row in ppn) else "FAIL",
            "detail": "light-bending and Shapiro q_R coefficients recorded",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_04_perihelion_coefficients",
            "result": "PASS" if any("(2 q_R - delta_beta)/3" in row["coefficient_value"] or "(2 q_R - delta_beta)/3" in row["derivation"] for row in ppn) else "FAIL",
            "detail": "perihelion coefficients match two-parameter q_R/delta_beta structure",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_05_clock_matter_nonparent",
            "result": "PASS" if all(row.get("parent_prediction_ready") == "False" for row in read_csv(PHENOMENOLOGY)) else "FAIL",
            "detail": "clock/matter rows remain non-parent predictions",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_06_rejection_ledger",
            "result": "PASS" if len(read_csv(REJECTIONS)) >= 6 else "FAIL",
            "detail": "unsupported coefficients rejected for scoring",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_07_readiness_translation_only",
            "result": "PASS" if any(row.get("translation_ready") == "True" and row.get("parent_prediction_ready") == "False" for row in readiness) else "FAIL",
            "detail": "translation-ready rows remain not parent-prediction-ready",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_08_runner_refuses_scoring",
            "result": "PASS" if any(row.get("current_status") == "REFUSED_NO_PARENT_PREDICTIONS" for row in read_csv(RUNNER)) else "FAIL",
            "detail": "runner refuses local-bound scoring",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_09_claim_gates_block",
            "result": "PASS" if all("BLOCKED" in row.get("status", "") or "TRANSLATION_ONLY" in row.get("status", "") or row.get("status", "").startswith("PASS") for row in read_csv(CLAIM_GATE)) else "FAIL",
            "detail": "derived local GR claim remains blocked and translation rows stay nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_10_decision_next",
            "result": "PASS" if any(row.get("result") == "NEXT_2232_TWO_PARAMETER_PPN_CONTROL_RUNNER_AND_ZERO_CONDITION_HUNT" for row in read_csv(DECISION)) else "FAIL",
            "detail": "decision selects two-parameter PPN control runner and zero-condition hunt next",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_11_next_target",
            "result": "PASS" if read_csv(NEXT_TARGET)[0]["next_target"].startswith("2232-Y5-R2FR-qR-delta-beta") else "FAIL",
            "detail": "next target is current-numbered q_R/delta_beta control runner",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_12_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2231 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_13_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated flags remain nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_14_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch copies written and parse",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_15_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_16_formalization_no_2231",
            "result": "PASS" if formalization_2231_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2231 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_17_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2231 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2231_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2231 imports response coefficient translations, keeps clock/matter/source/frame/R10/tracefree rows nonclaim, and selects q_R/delta_beta control runner plus zero-condition hunt next",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    ppn = transform_old_csv(SOURCE_FILES["1558_ppn_coefficients"])
    phen = transform_old_csv(SOURCE_FILES["1558_phenomenology"])
    readiness = transform_old_csv(SOURCE_FILES["1558_readiness"])
    rejections = transform_old_csv(SOURCE_FILES["1558_rejections"])
    runner = transform_old_csv(SOURCE_FILES["1558_runner"])
    claim = transform_old_csv(SOURCE_FILES["1558_claim"])
    decision = transform_old_csv(SOURCE_FILES["1558_decision"])
    next_target = transform_old_csv(SOURCE_FILES["1558_next"])

    write_csv(SOURCE_REGISTER, source)
    write_csv(PPN_COEFFICIENTS, ppn)
    write_csv(PHENOMENOLOGY, phen)
    write_csv(READINESS, readiness)
    write_csv(REJECTIONS, rejections)
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
            ppn,
            phen,
            readiness,
            rejections,
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
        raise SystemExit(f"2231 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
