from __future__ import annotations

import csv
import importlib.util
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
R10 = ROOT / "source-intake" / "r10"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1506-Y5-R10-RAB-source-test-charge-zero-or-executable-alpha-row.md"
START_TS = datetime.now(timezone.utc).timestamp()

RUNNER_SCRIPT = ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py"
RUNNER_OUT = ROOT / "runs" / "1506-R10-source-test-charge-template-runner" / "results"
VISUAL_BOUND_SOURCE = R10 / "derived" / "staging" / "R10_EotWash2020_alpha_lambda_VISUAL_NONCLAIM_1499.csv"

SOURCE_FILES = {
    "1505_validation": OUT / "P8_Y5_BRR545_1505_VALIDATION.csv",
    "1505_field_map": OUT / "P8_Y5_R10_1505_R10_RESIDUAL_FIELD_MAP_AUDIT.csv",
    "1505_theorem": OUT / "P8_Y5_R10_1505_QUOTIENT_VERTICAL_THEOREM_LEDGER.csv",
    "1505_beta_rows": OUT / "P8_Y5_R10_1505_BETA_BOUND_INPUT_ROWS_NONCLAIM.csv",
    "1505_alpha_routes": OUT / "P8_Y5_R10_1505_ALPHA_ROUTE_MATRIX.csv",
    "r10_curve_contract": ROOT / "runs" / "20260605-143500-Y5-R10-alpha-lambda-source-normalized-curve-data-or-no-range-theorem" / "results" / "P8_Y5_R10_MTS_CURVE_INPUT_CONTRACT.csv",
    "bulk_memory_fill": ROOT / "runs" / "20260605-142500-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill" / "results" / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_YUKAWA_FILL_ROW.csv",
    "runner_script": RUNNER_SCRIPT,
    "visual_bound_source": VISUAL_BOUND_SOURCE,
}

CURVE_TARGET = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
KERNEL_TARGET = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"
C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

CHARGE_ZERO_AUDIT = OUT / "P8_Y5_R10_1506_SOURCE_TEST_CHARGE_ZERO_AUDIT.csv"
CHARGE_THEOREM = OUT / "P8_Y5_R10_1506_SOURCE_TEST_CHARGE_THEOREM_LEDGER.csv"
ALPHA_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1506_SOURCE_TEST_CHARGE_TEMPLATE_NONCLAIM.csv"
BOUND_TEMPLATE = OUT / "R10_alpha_lambda_bound_curve_1506_VISUAL_RUNNER_SHAPE_NONCLAIM.csv"
RUNNER_LEDGER = OUT / "P8_Y5_R10_1506_RUNNER_LEDGER.csv"
ALPHA_INPUT_SCHEMA = OUT / "P8_Y5_R10_1506_ALPHA_INPUT_SCHEMA.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1506_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1506_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1506_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1506_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1506_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1506_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1506_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1506_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1506"
QUAR_AUDIT = QUARANTINE / "SOURCE_TEST_CHARGE_ZERO_AUDIT_NONCLAIM.csv"
QUAR_THEOREM = QUARANTINE / "SOURCE_TEST_CHARGE_THEOREM_LEDGER_NONCLAIM.csv"
QUAR_ALPHA = QUARANTINE / "R10_ALPHA_TEMPLATE_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "RUNNER_LEDGER_NONCLAIM.csv"
BRANCH_AUDIT = BRANCH_RESIDUALS / "r10_source_test_charge_zero_audit_nonclaim_1506.csv"
BRANCH_THEOREM = BRANCH_RESIDUALS / "r10_source_test_charge_theorem_ledger_nonclaim_1506.csv"
BRANCH_ALPHA = BRANCH_RESIDUALS / "r10_alpha_template_nonclaim_1506.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "r10_runner_ledger_nonclaim_1506.csv"

MTS_REQUIRED_COLUMNS = [
    "model_id",
    "branch_id",
    "curve_id",
    "lambda_value",
    "lambda_units",
    "alpha_predicted",
    "alpha_bound",
    "alpha_bound_source",
    "force_law_form",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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


def charge_zero_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CZ1506_0_source_charge_definition",
            "Q_X_source",
            "source charge coupling compact matter/source worldtube to X",
            "MISSING_PARENT_DEFINITION",
            "must be zero or numeric before alpha(lambda) score",
        ),
        (
            "CZ1506_1_test_charge_definition",
            "q_test_X",
            "test-body/readout charge coupling the R10 detector to X",
            "MISSING_PARENT_DEFINITION",
            "must be zero or numeric before alpha(lambda) score",
        ),
        (
            "CZ1506_2_zero_theorem_route",
            "Q_X_source=q_test_X=0",
            "charge-neutrality theorem for R10-active residual",
            "EXACT_CONDITIONAL_TARGET",
            "would kill alpha_X(lambda) even if X has a formal range",
        ),
        (
            "CZ1506_3_finite_route",
            "Q_X_source*q_test_X/(G_N M m)",
            "source-normalized finite Yukawa alpha product",
            "MISSING_NUMERIC_INPUTS",
            "requires same-frame source normalization and unit convention",
        ),
        (
            "CZ1506_4_boundary_projection",
            "boundary_flux and PiM_H_projection",
            "projection can source X even when bulk charge is zero",
            "MISSING_ZERO_OR_BOUND",
            "must be zero/bounded before local-GR/R10 pass",
        ),
        (
            "CZ1506_5_verdict",
            "alpha_X(lambda)",
            "R10 source/test charge status",
            "NOT_DERIVED_NOT_SCORE_READY",
            "emit runner-shaped nonclaim rows only",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "object": obj,
            "definition": definition,
            "current_status": status,
            "effect": effect,
            **flags(),
        }
        for audit_id, obj, definition, status, effect in rows
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1506_0_source_test_charge_zero",
            "statement": "If the R10-active residual has Q_X_source=0, q_test_X=0, zero boundary flux, zero Hamiltonian projection, and no local memory tail, then alpha_X(lambda)=0 for the R10 Yukawa comparison.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_sketch": "The Yukawa exchange amplitude is proportional to the product of source and test charges plus boundary/projection leakage. If every coupling channel is zero, the finite-range exchange has no R10 source.",
            "current_claim_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1506_1_charge_countermodel",
            "statement": "A quotient-vertical or beta-zero residual can still fail R10 if it has explicit source/test charge or boundary projection into the torsion-balance channel.",
            "proof_status": "COUNTERMODEL_ACTIVE",
            "proof_sketch": "Set beta_a=0 but keep Q_X_source and q_test_X finite in the Helmholtz Green function; alpha_X(lambda) remains finite.",
            "current_claim_status": "BLOCKS_BETA_ZERO_AS_R10_PASS",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1506_2_current_branch_verdict",
            "statement": "No parent-signed zero theorem or numeric coefficient pack exists for Q_X_source, q_test_X, beta_a, s_a, Z_a, or tau_R10; the runner-shaped alpha rows must remain nonclaim.",
            "proof_status": "DERIVED_AS_GATE_LOGIC",
            "proof_sketch": "Existing source contracts explicitly mark the required inputs missing and the generated runner rows are invalid by design.",
            "current_claim_status": "KEEP_EXECUTABLE_NONCLAIM_ALPHA_TEMPLATE",
            **flags(),
        },
    ]


def alpha_rows() -> list[dict[str, Any]]:
    anchor_rows = [
        ("3.86000000e-05", "1.00000000e+00", "text_threshold_anchor"),
        ("5.60000000e-05", "1.00000000e-01", "near_R10_smoke_anchor"),
        ("1.00000000e-04", "2.00000000e-02", "visual_mid_curve_anchor"),
    ]
    return [
        {
            "model_id": "MTS_1506_SOURCE_TEST_CHARGE_TEMPLATE_NONCLAIM",
            "branch_id": BRANCH_ID,
            "curve_id": f"MTS_1506_SOURCE_TEST_CHARGE_TEMPLATE_{label}",
            "lambda_value": lambda_value,
            "lambda_units": "m",
            "alpha_predicted": "MISSING_QX_QTEST_BETA_S_Z_PRODUCT",
            "alpha_bound": alpha_bound,
            "alpha_bound_source": rel(VISUAL_BOUND_SOURCE),
            "force_law_form": "alpha_X(lambda)=source_normalized_product_or_DERIVED_ZERO",
            "derivation_status": "template_invalid_missing_source_test_charge_and_parent_coefficients",
            "formula_reference": "alpha_X ~ Q_X_source q_test_X /(G_N M_source m_test) plus beta*s/Z readout branch",
            "source_file": "MISSING_SOURCE_FILE",
            "assumptions": "nonclaim row; replace every MISSING marker with parent-derived zero or source-backed numeric coefficient before scoring",
            "valid_for_claim": "false",
            "notes": f"runner-shaped nonclaim anchor {label}",
        }
        for lambda_value, alpha_bound, label in anchor_rows
    ]


def bound_rows() -> list[dict[str, Any]]:
    anchor_rows = [
        ("3.86000000e-05", "1.00000000e+00", "R10EW2020_text_threshold_anchor"),
        ("5.60000000e-05", "1.00000000e-01", "R10EW2020_visual_near_anchor"),
        ("1.00000000e-04", "2.00000000e-02", "R10EW2020_visual_mid_anchor"),
    ]
    return [
        {
            "bound_id": bound_id,
            "dataset_id": "EotWash_2020_fig5b1_visual_nonclaim_1506",
            "lambda_value": lambda_value,
            "lambda_units": "m",
            "alpha_bound": alpha_bound,
            "alpha_bound_source": rel(VISUAL_BOUND_SOURCE),
            "digitization_method": "visual_nonclaim_runner_shape_from_1499_staging",
            "source_file": rel(VISUAL_BOUND_SOURCE),
            "valid_for_claim": "false",
            "notes": "nonclaim runner-shape bound row; do not promote to live R10 curve",
        }
        for lambda_value, alpha_bound, bound_id in anchor_rows
    ]


def alpha_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "field": field,
            "required_value_or_policy": "required by R10 runner" if field in MTS_REQUIRED_COLUMNS else "extra",
            "current_status": "PRESENT_IN_1506_TEMPLATE",
            **flags(),
        }
        for field in MTS_REQUIRED_COLUMNS
    ]


def run_runner() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location("r10_runner_1506", RUNNER_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load R10 runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.run_runner(ALPHA_TEMPLATE, BOUND_TEMPLATE, RUNNER_OUT)
    return result["status"]


def runner_ledger_rows(status: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1506_0_template_runner",
            "mts_curve": status.get("mts_curve", ""),
            "bound_curve": status.get("bound_curve", ""),
            "output_dir": status.get("output_dir", ""),
            "valid_mts_rows": status.get("valid_mts_rows", ""),
            "valid_bound_rows": status.get("valid_bound_rows", ""),
            "R10_pass_for_claim": status.get("R10_pass_for_claim", False),
            "claim_allowed": status.get("claim_allowed", False),
            "interpretation": "expected block: template rows are runner-shaped but nonclaim and missing source/test coefficients",
            **flags(),
        }
    ]


def blocker_rows() -> list[dict[str, Any]]:
    blockers = [
        ("BLK1506_0_QX", "MISSING_Q_X_SOURCE_ZERO_OR_VALUE", "source charge is not parent-derived zero or numeric", "parent_action"),
        ("BLK1506_1_qtest", "MISSING_Q_TEST_X_ZERO_OR_VALUE", "test charge/readout is not parent-derived zero or numeric", "parent_action"),
        ("BLK1506_2_projection", "MISSING_HAMILTONIAN_PROJECTION_ZERO_OR_VALUE", "PiM_H projection may source R10 channel", "parent_action"),
        ("BLK1506_3_boundary", "MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND", "boundary flux remains a leakage path", "parent_action"),
        ("BLK1506_4_beta_s_Z", "MISSING_BETA_S_Z_PRODUCT", "matter readout/source/kinetic normalization product is missing", "parent_action"),
        ("BLK1506_5_kernel", "MISSING_R10_KERNEL", "R10 finite-source tau/kernel remains absent", rel(KERNEL_TARGET)),
        ("BLK1506_6_curve", "MISSING_REVIEWED_R10_CURVE", "visual bound rows are nonclaim; live curve remains absent", rel(CURVE_TARGET)),
        ("BLK1506_7_import", "MISSING_C_PARENT_IMPORT", "no live coefficient import exists", rel(C_PARENT_IMPORT)),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "blocking_marker": marker,
            "reason": reason,
            "target_path": target,
            **flags(),
        }
        for blocker_id, marker, reason, target in blockers
    ]


def simple_rows_from_blockers(blockers: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            f"{prefix}_id": f"{prefix.upper()}1506_{index}",
            "object": row["blocking_marker"],
            "path": row["target_path"],
            "status": "BLOCKED",
            "effect": row["reason"],
            **flags(),
        }
        for index, row in enumerate(blockers)
    ]


def c_parent_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CP1506_0_no_import",
            "path": rel(C_PARENT_IMPORT),
            "path_exists": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "1506 emits nonclaim alpha rows but refuses coefficient import without Q_X/q_test/beta/s/Z sources",
            "claim_effect": "R10/local-GR claim remains blocked",
            **flags(),
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        ("DEC1506_0_zero_theorem", "charge-zero theorem remains the cleanest route", "it would give alpha(lambda)=0 rather than fitting a tiny force"),
        ("DEC1506_1_template_runner", "use runner-shaped nonclaim rows for the fallback", "future coefficients can be inserted without schema drift"),
        ("DEC1506_2_next", "attack the no-range/positive-nohair route or fill source-backed coefficients", "one of these must close before R10 can score"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, rationale in decisions
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1506_0_1507",
            "next_target": "1507-Y5-R10-RAB-positive-nohair-charge-zero-or-source-backed-alpha-priors.md",
            "script": "scripts/Y5_R10_RAB_positive_nohair_charge_zero_or_source_backed_alpha_priors.py",
            "objective": "try to prove the R10-active residual has no local source/test charge by positive no-hair/operator silence; if not, prepare source-backed finite alpha priors",
            **flags(),
        }
    ]


def generated_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for column in ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]:
                value = row.get(column)
                if value not in (None, "", "False", "false", False):
                    return False
    return True


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (CHARGE_ZERO_AUDIT, QUAR_AUDIT),
        (CHARGE_THEOREM, QUAR_THEOREM),
        (ALPHA_TEMPLATE, QUAR_ALPHA),
        (RUNNER_LEDGER, QUAR_RUNNER),
        (CHARGE_ZERO_AUDIT, BRANCH_AUDIT),
        (CHARGE_THEOREM, BRANCH_THEOREM),
        (ALPHA_TEMPLATE, BRANCH_ALPHA),
        (RUNNER_LEDGER, BRANCH_RUNNER),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], status: dict[str, Any]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    alpha_schema_ok = set(read_csv(ALPHA_TEMPLATE)[0].keys()) >= set(MTS_REQUIRED_COLUMNS)
    alpha_rows_nonclaim = all(row["valid_for_claim"].lower() == "false" for row in read_csv(ALPHA_TEMPLATE))
    runner_blocked = status.get("R10_pass_for_claim") is False and status.get("claim_allowed") is False
    runner_files_exist = all((RUNNER_OUT / name).exists() for name in ["R10_runner_mts_validation.csv", "R10_runner_bound_validation.csv", "R10_runner_comparison.csv", "R10_runner_status.json"])
    live_targets_absent = not CURVE_TARGET.exists() and not KERNEL_TARGET.exists()
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = all(parse_csv(path) for path in generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_AUDIT, QUAR_THEOREM, QUAR_ALPHA, QUAR_RUNNER, BRANCH_AUDIT, BRANCH_THEOREM, BRANCH_ALPHA, BRANCH_RUNNER])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1506_0_local_sources", source_paths_exist, "all cited source/test/R10 source paths exist"),
        ("VAL1506_1_alpha_schema", alpha_schema_ok, "MTS alpha template has runner-required columns"),
        ("VAL1506_2_alpha_nonclaim", alpha_rows_nonclaim, "all alpha rows remain valid_for_claim=false"),
        ("VAL1506_3_runner_blocked", runner_blocked, "R10 runner blocks the nonclaim template as expected"),
        ("VAL1506_4_runner_files", runner_files_exist, "runner validation/comparison files written"),
        ("VAL1506_5_live_targets_absent", live_targets_absent, "live R10 curve/kernel targets remain absent"),
        ("VAL1506_6_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1506_7_csv_parse", csv_parse_ok, "all generated 1506 CSVs parse cleanly"),
        ("VAL1506_8_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1506_9_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1506_10_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1506_11_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1506_12_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1506 built runner-shaped alpha rows and verified the runner blocks them until source/test charges are real"
            if overall
            else "1506 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    charge_rows: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1506 - Source/Test Charge Zero or Executable Alpha Row",
                "",
                "## Verdict",
                "- R10 can only be theorem-zero if Q_X_source, q_test_X, boundary flux, Hamiltonian projection, and local memory tail are all zero.",
                "- That zero theorem is exact but not parent-signed; the finite route still lacks Q_X, q_test, beta, s, Z, tau_R10, and reviewed bound rows.",
                "- A runner-shaped alpha(lambda) template was generated and the R10 runner correctly blocks it as nonclaim.",
                "",
                "## Source/Test Charge Audit",
                md_table(charge_rows, ["audit_id", "object", "current_status", "effect"]),
                "",
                "## Charge Theorem Ledger",
                md_table(theorem, ["theorem_id", "proof_status", "current_claim_status"]),
                "",
                "## Runner Ledger",
                md_table(runner_rows, ["runner_id", "valid_mts_rows", "valid_bound_rows", "R10_pass_for_claim", "interpretation"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    charge_rows = charge_zero_rows()
    theorem = theorem_rows()
    alpha_template = alpha_rows()
    bound_template = bound_rows()
    alpha_schema = alpha_schema_rows()
    blockers = blocker_rows()
    readiness = simple_rows_from_blockers(blockers, "ready")
    c_parent = c_parent_refusal_rows()
    local_rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LRS1506_0",
            "object": "R10 source/test charge branch",
            "status": "SOURCE_TEST_ZERO_OR_ALPHA_PRIORS_REQUIRED",
            "effect": "runner-shaped fallback exists, but no local-GR/Newton/R10 claim",
            **flags(),
        }
    ]
    rejections = simple_rows_from_blockers(blockers, "rejection")
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(CHARGE_ZERO_AUDIT, charge_rows)
    write_csv(CHARGE_THEOREM, theorem)
    write_csv(ALPHA_TEMPLATE, alpha_template)
    write_csv(BOUND_TEMPLATE, bound_template)
    write_csv(ALPHA_INPUT_SCHEMA, alpha_schema)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(C_PARENT_REFUSAL, c_parent)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    status = run_runner()
    runner_rows = runner_ledger_rows(status)
    write_csv(RUNNER_LEDGER, runner_rows)
    copy_outputs()

    generated_csvs = [
        CHARGE_ZERO_AUDIT,
        CHARGE_THEOREM,
        ALPHA_TEMPLATE,
        BOUND_TEMPLATE,
        RUNNER_LEDGER,
        ALPHA_INPUT_SCHEMA,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, status)
    write_csv(VALIDATION, validation)
    write_doc(charge_rows, theorem, runner_rows, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
