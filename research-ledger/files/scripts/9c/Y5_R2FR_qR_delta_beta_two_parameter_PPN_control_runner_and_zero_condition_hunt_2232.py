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
DOC = ROOT / "2232-Y5-R2FR-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_QR_BETA_CONTROL_RUNNER_2232"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2231_doc": ROOT / "2231-Y5-R2FR-qR-beta-matter-clock-coefficient-source-map-or-rejection.md",
    "2231_validation": OUT / "P8_Y5_BRR545_2231_VALIDATION.csv",
    "2231_next": OUT / "P8_Y5_PARENT_QLOC_2231_NEXT_TARGET.csv",
    "1559_doc": ROOT / "1559-Y5-qR-delta-beta-two-parameter-PPN-control-runner-and-zero-condition-hunt.md",
    "1559_validation": OUT / "P8_Y5_BRR545_1559_VALIDATION.csv",
    "1559_model": OUT / "P8_Y5_PARENT_QLOC_1559_TWO_PARAMETER_MODEL.csv",
    "1559_bound_box": OUT / "P8_Y5_PARENT_QLOC_1559_PARAMETER_BOUND_BOX_NONCLAIM.csv",
    "1559_zero_hunt": OUT / "P8_Y5_PARENT_QLOC_1559_PARENT_ZERO_CONDITION_HUNT.csv",
    "1559_runner": OUT / "P8_Y5_PARENT_QLOC_1559_TWO_PARAMETER_CONTROL_RUNNER_NONCLAIM.csv",
    "1559_claim": OUT / "P8_Y5_PARENT_QLOC_1559_CLAIM_GATE.csv",
    "1559_decision": OUT / "P8_Y5_PARENT_QLOC_1559_DECISION.csv",
    "1559_next": OUT / "P8_Y5_PARENT_QLOC_1559_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2232_SOURCE_REGISTER.csv"
TWO_PARAMETER_MODEL = OUT / "P8_Y5_PARENT_QLOC_2232_TWO_PARAMETER_MODEL.csv"
PARAMETER_BOUND_BOX = OUT / "P8_Y5_PARENT_QLOC_2232_PARAMETER_BOUND_BOX_NONCLAIM.csv"
ZERO_CONDITION_HUNT = OUT / "P8_Y5_PARENT_QLOC_2232_PARENT_ZERO_CONDITION_HUNT.csv"
CONTROL_RUNNER = OUT / "P8_Y5_PARENT_QLOC_2232_TWO_PARAMETER_CONTROL_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2232_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2232_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2232_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2232_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2232_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2232_QR_BETA_CONTROL_RUNNER_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "qR_beta_control_runner_nonclaim_2232.csv",
    "beta_docs": BETA_DOCS / "QR_BETA_CONTROL_RUNNER_2232_NONCLAIM.csv",
}


OLD_TO_NEW = [
    ("1560-Y5-parent-weak-field-zero-condition-derivation-or-demotion.md", "2233-Y5-R2FR-parent-weak-field-zero-condition-derivation-or-demotion.md"),
    ("scripts/Y5_parent_weak_field_zero_condition_derivation_or_demotion.py", "scripts/Y5_R2FR_parent_weak_field_zero_condition_derivation_or_demotion_2233.py"),
    ("NEXT_1560_PARENT_WEAK_FIELD_ZERO_CONDITION_DERIVATION", "NEXT_2233_PARENT_WEAK_FIELD_ZERO_CONDITION_DERIVATION"),
    ("NEXT_1560", "NEXT_2233"),
    ("1560", "2233"),
    ("1559", "2232"),
    ("1558", "2231"),
    ("1557", "2230"),
    ("1556", "2229"),
]


GENERATED = [
    SOURCE_REGISTER,
    TWO_PARAMETER_MODEL,
    PARAMETER_BOUND_BOX,
    ZERO_CONDITION_HUNT,
    CONTROL_RUNNER,
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


def formalization_2232_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2232" in path.name
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
        role = "current coefficient source-map handoff" if key.startswith("2231") else "older two-parameter PPN control evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2232_{index}_{key}",
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
        shutil.copyfile(ZERO_CONDITION_HUNT, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(ZERO_CONDITION_HUNT),
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
    model: list[dict[str, Any]],
    bound_box: list[dict[str, Any]],
    zero_hunt: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2232 - Y5/R2FR q_R/delta_beta Two-Parameter PPN Control Runner And Zero-Condition Hunt",
            "## Verdict\n"
            "- 2232 imports the old `1559` q_R/delta_beta two-parameter PPN control runner into the current R2FR line.\n"
            "- The control plane is now explicit: `q_R` maps to `gamma-1`, `delta_beta` maps to `beta-1`, and Mercury tracks the degeneracy `(2 q_R - delta_beta)/3`.\n"
            "- The runner can reject hypothetical leak vectors, including oversized `q_R` and oversized `delta_beta`, but it cannot score MTS because the parent action has not produced the vector.\n"
            "- The parent zero-condition hunt is now the real derivation target: force `R_AB=O(L^2)`, kill reciprocal charge, supply matter descent, derive second-order beta completion, and suppress extra local modes.\n"
            "- Next target is the parent weak-field zero-condition derivation or demotion.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Two-Parameter Model\n"
            + md_table(model, ["model_id", "observable_response", "leak_parameter", "coefficient", "units", "model_status"]),
            "## Parameter Bound Box\n"
            + md_table(bound_box, ["bound_id", "parameter_or_combo", "local_bound_rows", "measured_or_central", "one_sigma", "control_bound", "bound_status"]),
            "## Control Runner\n"
            + md_table(runner, ["case_id", "label", "q_R_input", "delta_beta_input", "gamma_minus_1", "beta_minus_1", "mercury_residual_arcsec_per_century", "control_status"]),
            "## Parent Zero-Condition Hunt\n"
            + md_table(zero_hunt, ["zero_id", "target_zero", "required_statement", "mathematical_content", "status", "next_derivation_step"]),
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
            "This gives the local branch a useful control dashboard, not a trophy. If a future parent derivation predicts `q_R` and `delta_beta`, this runner tells us immediately whether the values survive gamma, beta, light/Shapiro, and perihelion constraints. Until then, the important work is not fitting the control plane; it is deriving why the parent theory lands at or near the GR origin.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    model = read_csv(TWO_PARAMETER_MODEL)
    runner = read_csv(CONTROL_RUNNER)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) else "FAIL",
            "detail": "all cited 2232 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2231_validation"]) and validation_pass(SOURCE_FILES["1559_validation"]) else "FAIL",
            "detail": "2231 and 1559 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_02_model_q_beta",
            "result": "PASS" if any(row["leak_parameter"] == "q_R" and row["coefficient"] == "1" for row in model) and any(row["leak_parameter"] == "delta_beta" and row["coefficient"] == "1" for row in model) else "FAIL",
            "detail": "q_R and delta_beta unit translation rows present",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_03_model_perihelion_combo",
            "result": "PASS" if any(row["coefficient"] == "(2 q_R - delta_beta)/3" for row in model) else "FAIL",
            "detail": "perihelion degeneracy model present",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_04_bound_box",
            "result": "PASS" if len(read_csv(PARAMETER_BOUND_BOX)) >= 3 else "FAIL",
            "detail": "q_R and delta_beta bound box written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_05_GR_origin_passes",
            "result": "PASS" if any(row["label"] == "GR/null closure origin" and row["control_status"] == "PASS_CONTROL_BOX" for row in runner) else "FAIL",
            "detail": "GR origin passes control box",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_06_q_fail_fails",
            "result": "PASS" if any(row["label"] == "q_R too large" and row["control_status"] == "FAIL_CONTROL_BOX" for row in runner) else "FAIL",
            "detail": "oversized q_R fails Cassini/gamma bound",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_07_degeneracy_line",
            "result": "PASS" if any(row["label"] == "perihelion degeneracy line" and row["mercury_residual_arcsec_per_century"] == "0" for row in runner) else "FAIL",
            "detail": "perihelion degeneracy example has zero Mercury residual",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_08_zero_conditions",
            "result": "PASS" if len(read_csv(ZERO_CONDITION_HUNT)) >= 6 else "FAIL",
            "detail": "parent zero-condition hunt ledger written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_09_claim_gates",
            "result": "PASS" if all("BLOCKED" in row.get("status", "") or row.get("status", "").startswith("PASS") for row in read_csv(CLAIM_GATE)) else "FAIL",
            "detail": "local GR derivation remains blocked",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_10_decision_next",
            "result": "PASS" if any(row.get("result") == "NEXT_2233_PARENT_WEAK_FIELD_ZERO_CONDITION_DERIVATION" for row in read_csv(DECISION)) else "FAIL",
            "detail": "decision selects parent weak-field zero-condition derivation next",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_11_next_target",
            "result": "PASS" if read_csv(NEXT_TARGET)[0]["next_target"].startswith("2233-Y5-R2FR-parent-weak-field") else "FAIL",
            "detail": "next target is parent weak-field zero-condition derivation or demotion",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_12_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2232 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_13_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated flags remain nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_14_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch copies written and parse",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_15_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_16_formalization_no_2232",
            "result": "PASS" if formalization_2232_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2232 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_17_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2232 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2232_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2232 imports q_R/delta_beta two-parameter PPN control runner and zero-condition hunt while keeping local predictions blocked",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    model = transform_old_csv(SOURCE_FILES["1559_model"])
    bound_box = transform_old_csv(SOURCE_FILES["1559_bound_box"])
    zero_hunt = transform_old_csv(SOURCE_FILES["1559_zero_hunt"])
    runner = transform_old_csv(SOURCE_FILES["1559_runner"])
    claim = transform_old_csv(SOURCE_FILES["1559_claim"])
    decision = transform_old_csv(SOURCE_FILES["1559_decision"])
    next_target = transform_old_csv(SOURCE_FILES["1559_next"])

    write_csv(SOURCE_REGISTER, source)
    write_csv(TWO_PARAMETER_MODEL, model)
    write_csv(PARAMETER_BOUND_BOX, bound_box)
    write_csv(ZERO_CONDITION_HUNT, zero_hunt)
    write_csv(CONTROL_RUNNER, runner)
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
            model,
            bound_box,
            zero_hunt,
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
        raise SystemExit(f"2232 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
