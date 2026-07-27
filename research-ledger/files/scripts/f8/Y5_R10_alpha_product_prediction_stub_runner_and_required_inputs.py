from __future__ import annotations

import csv
import json
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import MTS_REQUIRED_COLUMNS, run_runner


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1060-Y5-R10-alpha-product-prediction-stub-runner-and-required-inputs.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1060-alpha-product-prediction-stub-runner" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
R10_RUN_DIR = RUN_DIR / "r10_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1060_ALPHA_PRODUCT_PREDICTION_TEMPLATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1060_ALPHA_PRODUCT_BOUND_IMPORT.csv"
MTS_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_1060_ALPHA_PRODUCT_RUNNER_TEMPLATE_NONCLAIM.csv"
BOUND_CANDIDATE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"

PRODUCT_REQUIRED_COLUMNS = [
    "prediction_id",
    "arena",
    "product_symbol",
    "product_value",
    "product_units",
    "product_source",
    "inputs_present",
    "required_inputs",
    "derivation_status",
    "valid_for_claim",
    "notes",
]

BOUND_REQUIRED_COLUMNS = [
    "bound_id",
    "arena",
    "product_symbol",
    "bound_value",
    "bound_units",
    "bound_source",
    "source_row",
    "bound_type",
    "valid_for_claim",
    "notes",
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def has_missing_marker(row: dict[str, str]) -> bool:
    joined = json.dumps(row, sort_keys=True)
    return "MISSING" in joined or "PLACEHOLDER" in joined or "template_invalid" in joined


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1060_0_1059_next", "source-intake/mts_residuals/P8_Y5_R10_1059_NEXT_TARGET.csv", "1060-Y5-R10-alpha-product-prediction-stub-runner-and-required-inputs.md", "1059 handoff."),
        ("SRC1060_1_1059_pack", "source-intake/mts_residuals/P8_Y5_R10_1059_ALPHA_PRODUCT_PRIOR_PACK.csv", "APP1059_0_clock_YbE3E2", "alpha product-prior pack."),
        ("SRC1060_2_1059_transfer", "source-intake/mts_residuals/P8_Y5_R10_1059_NO_TRANSFER_GATES.csv", "NTG1059_1_clock_to_WEP", "no-transfer gates."),
        ("SRC1060_3_1059_debt", "source-intake/mts_residuals/P8_Y5_R10_1059_PROJECTION_DEBT_LEDGER.csv", "PD1059_2_tau_WEP", "projection debt ledger."),
        ("SRC1060_4_1059_rules", "source-intake/mts_residuals/P8_Y5_R10_1059_PRODUCT_ONLY_SCORE_RULES.csv", "PSR1059_3_claim_validity", "product-only score rules."),
        ("SRC1060_5_1052_clock", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv", "ACB1052_2", "clock product bound source."),
        ("SRC1060_6_1052_WEP", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", "AWP1052_0_alpha_Coulomb", "WEP product target source."),
        ("SRC1060_7_1052_R10", "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_R10_PROJECTION_LEDGER.csv", "RAP1052_0_product_law", "R10 finite branch schema."),
        ("SRC1060_8_1053_tau", "source-intake/mts_residuals/P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv", "TPR1053_4_verdict", "tau projection debt."),
        ("SRC1060_9_1053_KX", "source-intake/mts_residuals/P8_Y5_R10_1053_KX_ZX_PLACEHOLDER_LEDGER.csv", "KZ1053_3_KX_R10", "KX/ZX/lambda debt."),
        ("SRC1060_10_R10_bound_candidate", "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv", "R10_VECTOR_2020_REVIEW_0000", "R10 review-candidate curve."),
        ("SRC1060_11_R10_runner", "scripts/R10_alpha_lambda_bound_prediction_runner.py", "MTS_REQUIRED_COLUMNS", "existing R10 runner."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def schema_rows() -> list[dict[str, str]]:
    definitions = {
        "prediction_id": "stable row id",
        "arena": "clock, MICROSCOPE_WEP, R10_short_range, or cross_arena",
        "product_symbol": "exact product being predicted; runner may not algebraically split it",
        "product_value": "numeric predicted product value only; no placeholders or derived-by-division values",
        "product_units": "yr^-1, dimensionless, or dimensionless alpha(lambda) convention",
        "product_source": "local source path for the prediction derivation",
        "inputs_present": "semicolon-separated concrete input names that are numeric/sourced",
        "required_inputs": "semicolon-separated input names required for this product",
        "derivation_status": "DERIVED_NUMERIC, SYMBOLIC_ONLY, or MISSING_* status",
        "valid_for_claim": "true only after all required inputs, numeric values, and source paths are real",
        "notes": "nonclaim caveats",
    }
    return [
        {
            "column": column,
            "definition": definitions[column],
            "required": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for column in PRODUCT_REQUIRED_COLUMNS
    ]


def required_input_rows() -> list[dict[str, str]]:
    return [
        {
            "input_id": "REQ1060_0_clock_product",
            "arena": "clock",
            "product_symbol": "P_clock_alpha",
            "required_numeric_inputs": "b_alpha_counterterm;tau_clock_time OR directly derived P_clock_alpha",
            "currently_available": "source-backed bound only, no MTS product prediction",
            "missing_status": "MISSING_MTS_PRODUCT_PREDICTION",
            "blocks": "clock product comparison as MTS prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "REQ1060_1_WEP_alpha",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "required_numeric_inputs": "beta_source_alpha;b_alpha_counterterm;tau_WEP OR directly derived P_WEP_alpha",
            "currently_available": "source-backed product target only",
            "missing_status": "MISSING_BETA_SOURCE_ALPHA_AND_TAU_WEP",
            "blocks": "WEP alpha product prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "REQ1060_2_WEP_surface",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_surface",
            "required_numeric_inputs": "beta_source_or_binding;b_A;tau_WEP OR directly derived P_WEP_surface",
            "currently_available": "source-backed robust target only",
            "missing_status": "MISSING_BINDING_OWNER_AND_TAU_WEP",
            "blocks": "robust WEP product prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "input_id": "REQ1060_3_R10_alpha",
            "arena": "R10_short_range",
            "product_symbol": "P_R10_alpha(lambda)",
            "required_numeric_inputs": "lambda_X;Z_X;K_X^R10(lambda);beta_s(lambda);beta_t(lambda);tau_R10;epsilon_tail;promoted alpha_bound(lambda)",
            "currently_available": "schema plus review-candidate nonclaim bound curve",
            "missing_status": "MISSING_R10_FINITE_BRANCH_INPUTS",
            "blocks": "R10 alpha(lambda) product comparison",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_template_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1060_0_clock_alpha_template",
            "arena": "clock",
            "product_symbol": "P_clock_alpha",
            "product_value": "MISSING_DERIVED_P_CLOCK_ALPHA",
            "product_units": "yr^-1",
            "product_source": "MISSING_SOURCE_FILE",
            "inputs_present": "none",
            "required_inputs": "b_alpha_counterterm;tau_clock_time OR directly derived P_clock_alpha",
            "derivation_status": "MISSING_MTS_PRODUCT_PREDICTION",
            "valid_for_claim": "false",
            "notes": "Clock bound exists; MTS product prediction does not.",
        },
        {
            "prediction_id": "PRED1060_1_WEP_alpha_template",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "product_value": "MISSING_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "MISSING_SOURCE_FILE",
            "inputs_present": "none",
            "required_inputs": "beta_source_alpha;b_alpha_counterterm;tau_WEP OR directly derived P_WEP_alpha",
            "derivation_status": "MISSING_BETA_SOURCE_ALPHA_AND_TAU_WEP",
            "valid_for_claim": "false",
            "notes": "WEP target exists; no MTS predicted product exists.",
        },
        {
            "prediction_id": "PRED1060_2_R10_alpha_template",
            "arena": "R10_short_range",
            "product_symbol": "P_R10_alpha(lambda)",
            "product_value": "MISSING_KX_BETA_SOURCE_BETA_TEST_TAU_R10_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "MISSING_SOURCE_FILE",
            "inputs_present": "none",
            "required_inputs": "lambda_X;Z_X;K_X^R10(lambda);beta_s(lambda);beta_t(lambda);tau_R10;epsilon_tail",
            "derivation_status": "MISSING_R10_FINITE_BRANCH_INPUTS",
            "valid_for_claim": "false",
            "notes": "R10 row must remain invalid until finite branch inputs and claim-valid bound curve exist.",
        },
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1060_0_clock_YbE3E2",
            "arena": "clock",
            "product_symbol": "P_clock_alpha",
            "bound_value": "2.1e-18",
            "bound_units": "yr^-1",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
            "source_row": "ACB1052_2",
            "bound_type": "upper_abs_1sigma_product_bound",
            "valid_for_claim": "false",
            "notes": "source-backed product bound, not standalone b_alpha",
        },
        {
            "bound_id": "BOUND1060_1_WEP_alpha",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "bound_value": "4.797780522732e-05",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
            "source_row": "AWP1052_0_alpha_Coulomb",
            "bound_type": "required_abs_product_max_smoke_convention",
            "valid_for_claim": "false",
            "notes": "target only until full material/tau/source convention is derived",
        },
        {
            "bound_id": "BOUND1060_2_WEP_surface",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_surface",
            "bound_value": "2.887280314062e-05",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
            "source_row": "AWP1052_1_surface_binding",
            "bound_type": "required_abs_product_max_smoke_convention",
            "valid_for_claim": "false",
            "notes": "robust target if surface/binding branch survives",
        },
        {
            "bound_id": "BOUND1060_3_R10_alpha",
            "arena": "R10_short_range",
            "product_symbol": "P_R10_alpha(lambda)",
            "bound_value": "MISSING_PROMOTED_ALPHA_BOUND_CURVE",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "source_row": "R10_VECTOR_2020_REVIEW_0000",
            "bound_type": "review_candidate_only",
            "valid_for_claim": "false",
            "notes": "not a claim-valid R10 bound row",
        },
    ]


def validate_prediction_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not rows:
        return [{"row_index": "schema", "prediction_id": "", "validation_status": "invalid", "issues": "file_has_no_rows"}]
    missing_columns = [column for column in PRODUCT_REQUIRED_COLUMNS if column not in rows[0]]
    if missing_columns:
        return [{"row_index": "schema", "prediction_id": "", "validation_status": "invalid", "issues": "missing_column:" + ";".join(missing_columns)}]
    for index, row in enumerate(rows):
        issues: list[str] = []
        value = parse_float(row.get("product_value", ""))
        if value is None:
            issues.append("product_value_not_numeric")
        if has_missing_marker(row):
            issues.append("missing_or_placeholder_marker_present")
        if row.get("inputs_present", "").strip().lower() in {"", "none"}:
            issues.append("no_inputs_present")
        if not flag(row.get("valid_for_claim", "")):
            issues.append("valid_for_claim_not_true")
        source = row.get("product_source", "")
        if flag(row.get("valid_for_claim", "")) and source and not source.startswith(("http://", "https://")):
            if not source_path(source).exists():
                issues.append("prediction_source_missing")
        out.append(
            {
                "row_index": index,
                "prediction_id": row.get("prediction_id", ""),
                "arena": row.get("arena", ""),
                "product_symbol": row.get("product_symbol", ""),
                "product_value": value if value is not None else "",
                "valid_for_claim": row.get("valid_for_claim", ""),
                "validation_status": "valid" if not issues else "invalid",
                "issues": ";".join(issues),
            }
        )
    return out


def validate_bound_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not rows:
        return [{"row_index": "schema", "bound_id": "", "validation_status": "invalid", "issues": "file_has_no_rows"}]
    missing_columns = [column for column in BOUND_REQUIRED_COLUMNS if column not in rows[0]]
    if missing_columns:
        return [{"row_index": "schema", "bound_id": "", "validation_status": "invalid", "issues": "missing_column:" + ";".join(missing_columns)}]
    for index, row in enumerate(rows):
        issues: list[str] = []
        value = parse_float(row.get("bound_value", ""))
        if value is None or (value is not None and value <= 0):
            issues.append("bound_value_not_positive_numeric")
        if has_missing_marker(row):
            issues.append("missing_or_placeholder_marker_present")
        if row.get("bound_source", "") and not row.get("bound_source", "").startswith(("http://", "https://")):
            if not source_path(row["bound_source"]).exists():
                issues.append("bound_source_missing")
        out.append(
            {
                "row_index": index,
                "bound_id": row.get("bound_id", ""),
                "arena": row.get("arena", ""),
                "product_symbol": row.get("product_symbol", ""),
                "bound_value": value if value is not None else "",
                "valid_for_claim": row.get("valid_for_claim", ""),
                "validation_status": "valid_nonclaim_bound" if not issues else "invalid",
                "issues": ";".join(issues),
            }
        )
    return out


def compare_product_rows(prediction_validation: list[dict[str, Any]], bound_validation: list[dict[str, Any]]) -> list[dict[str, Any]]:
    valid_predictions = [row for row in prediction_validation if row.get("validation_status") == "valid"]
    valid_bounds = [row for row in bound_validation if str(row.get("validation_status", "")).startswith("valid")]
    if not valid_predictions:
        return [
            {
                "comparison_id": "PRODUCT_COMPARE_NO_VALID_PREDICTIONS",
                "arena": "",
                "product_symbol": "",
                "product_value": "",
                "bound_value": "",
                "comparison_status": "not_run",
                "pass_for_claim": "false",
                "issues": "no valid MTS alpha product prediction rows",
            }
        ]
    rows: list[dict[str, Any]] = []
    for prediction in valid_predictions:
        matches = [
            bound
            for bound in valid_bounds
            if bound.get("arena") == prediction.get("arena") and bound.get("product_symbol") == prediction.get("product_symbol")
        ]
        if not matches:
            rows.append(
                {
                    "comparison_id": f"PRODUCT_COMPARE_NO_BOUND_{prediction.get('prediction_id')}",
                    "arena": prediction.get("arena", ""),
                    "product_symbol": prediction.get("product_symbol", ""),
                    "product_value": prediction.get("product_value", ""),
                    "bound_value": "",
                    "comparison_status": "not_run",
                    "pass_for_claim": "false",
                    "issues": "no matching product bound row",
                }
            )
            continue
        bound = matches[0]
        product_value = float(prediction["product_value"])
        bound_value = float(bound["bound_value"])
        passed = abs(product_value) <= bound_value and flag(prediction.get("valid_for_claim", "")) and flag(bound.get("valid_for_claim", ""))
        rows.append(
            {
                "comparison_id": f"PRODUCT_COMPARE_{prediction.get('prediction_id')}_{bound.get('bound_id')}",
                "arena": prediction.get("arena", ""),
                "product_symbol": prediction.get("product_symbol", ""),
                "product_value": product_value,
                "bound_value": bound_value,
                "comparison_status": "compared_nonclaim" if not passed else "compared_claim_ready",
                "pass_for_claim": str(passed).lower(),
                "issues": "" if passed else "prediction_or_bound_not_claim_valid_or_value_exceeds_bound",
            }
        )
    return rows


def run_product_runner(prediction_file: Path, bound_file: Path, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    prediction_rows = read_csv(prediction_file)
    bound_rows = read_csv(bound_file)
    prediction_validation = validate_prediction_rows(prediction_rows)
    bound_validation = validate_bound_rows(bound_rows)
    comparisons = compare_product_rows(prediction_validation, bound_validation)
    passed = [row for row in comparisons if row.get("pass_for_claim") == "true"]
    blocked = [row for row in comparisons if row.get("pass_for_claim") != "true"]
    status = {
        "generated_at_utc": stamp(),
        "prediction_rows": len(prediction_rows),
        "bound_rows": len(bound_rows),
        "valid_prediction_rows": len([row for row in prediction_validation if row.get("validation_status") == "valid"]),
        "valid_bound_rows": len([row for row in bound_validation if str(row.get("validation_status", "")).startswith("valid")]),
        "comparison_rows": len(comparisons),
        "passed_rows": len(passed),
        "blocked_or_failed_rows": len(blocked),
        "claim_allowed": bool(comparisons) and bool(passed) and not blocked,
    }
    write_csv(output_dir / "alpha_product_prediction_validation.csv", prediction_validation)
    write_csv(output_dir / "alpha_product_bound_validation.csv", bound_validation)
    write_csv(output_dir / "alpha_product_comparison.csv", comparisons)
    (output_dir / "alpha_product_runner_status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return {
        "status": status,
        "prediction_validation": prediction_validation,
        "bound_validation": bound_validation,
        "comparisons": comparisons,
    }


def strict_failure_rows(product_status: dict[str, Any], r10_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "failure_id": "SFR1060_0_missing_product_predictions",
            "object": "alpha product prediction template",
            "expected_failure": "valid_prediction_rows=0",
            "observed_status": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "meaning": "runner refuses missing tau/source/KX placeholder rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "failure_id": "SFR1060_1_no_standalone_claim",
            "object": "standalone b_alpha or beta_source_alpha",
            "expected_failure": "not represented as scoreable products",
            "observed_status": "standalone claims absent from prediction schema",
            "meaning": "runner cannot divide by guessed tau/source factors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "failure_id": "SFR1060_2_R10_runner",
            "object": "R10 alpha(lambda) smoke row",
            "expected_failure": "valid_mts_rows=0",
            "observed_status": f"valid_mts_rows={r10_status.get('valid_mts_rows')}; valid_bound_rows={r10_status.get('valid_bound_rows')}",
            "meaning": "existing R10 runner refuses finite-branch placeholders",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def product_runner_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1060_0_alpha_product_stub",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject placeholder predictions and keep claim false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def r10_runner_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "smoke_id": "SMOKE1060_0_R10_runner_refusal",
            "valid_mts_rows": str(status.get("valid_mts_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "R10_pass_for_claim": str(status.get("R10_pass_for_claim", "")).lower(),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject R10 alpha product placeholders until prediction inputs are sourced",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1060_0_product_runner_claim",
            "claim": "alpha product runner has scoreable MTS predictions",
            "gate_pass": "false",
            "reason": "prediction template contains missing tau/source/KX inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1060_1_clock",
            "claim": "clock product prediction is tested",
            "gate_pass": "false",
            "reason": "source-backed clock bound exists but MTS P_clock_alpha prediction is missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1060_2_WEP",
            "claim": "WEP alpha product prediction is tested",
            "gate_pass": "false",
            "reason": "P_WEP_alpha prediction and tau_WEP/beta_source inputs are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1060_3_R10",
            "claim": "R10 alpha(lambda) product prediction is tested",
            "gate_pass": "false",
            "reason": "R10 finite branch inputs and promoted bound curve are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1060_0_runner_built",
            "decision": "alpha product-prediction runner schema now exists",
            "because": "prediction rows, bound rows, validations, and comparisons are generated",
            "next_action": "fill one product prediction input set rather than claiming from bounds alone",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1060_1_runner_refuses",
            "decision": "runner correctly refuses all current MTS placeholder predictions",
            "because": "valid prediction rows are zero and missing markers remain",
            "next_action": "source tau_WEP/beta_source_alpha first, or derive P_WEP_alpha directly",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1060_2_best_next",
            "decision": "next target is the first WEP alpha product input fill",
            "because": "WEP has the clearest numeric product target and the missing inputs are explicitly named",
            "next_action": "1061-Y5-R10-WEP-alpha-product-first-input-fill-tauWEP-betaSource-material-map.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1061-Y5-R10-WEP-alpha-product-first-input-fill-tauWEP-betaSource-material-map.md",
            "objective": "try to fill the first scoreable WEP alpha product prediction input set by deriving or sourcing beta_source_alpha, tau_WEP, and the material convention for P_WEP_alpha, while keeping the product target nonclaim unless all inputs are real",
            "include": "tau_WEP definition source, beta_source_alpha source/theorem route, material convention, product prediction row, failure if any input is missing",
            "exclude": "standalone b_alpha claim, guessed tau values, unity shortcuts, cancellation, public WEP/R10/clock/local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def mts_template_rows() -> list[dict[str, str]]:
    row = {
        "model_id": "MTS_source_normalized_Newton_branch",
        "branch_id": "alpha_product_prediction_stub_runner_template",
        "curve_id": "MTS_1060_alpha_product_prediction_stub_nonclaim",
        "lambda_value": "MISSING_R10_LAMBDA_X",
        "lambda_units": "m",
        "alpha_predicted": "MISSING_R10_PRODUCT_PREDICTION",
        "alpha_bound": "MISSING_PROMOTED_BOUND",
        "alpha_bound_source": str(BOUND_CANDIDATE),
        "force_law_form": "R10 product prediction requires K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)+epsilon_tail(lambda)",
        "derivation_status": "template_invalid_product_prediction_inputs_missing",
        "formula_reference": "P8_Y5_R10_1060_ALPHA_PRODUCT_PREDICTION_TEMPLATE_NONCLAIM.csv",
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_1060_ALPHA_PRODUCT_PREDICTION_TEMPLATE_NONCLAIM.csv",
        "assumptions": "nonclaim placeholder; product-only; no unity tau; no cancellation",
        "valid_for_claim": "false",
        "notes": "Existing R10 runner must refuse this row until finite branch inputs and bound curve are claim-valid.",
    }
    return [{column: row[column] for column in MTS_REQUIRED_COLUMNS}]


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_time = STARTED.timestamp()
    for path in FORMALIZATION.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime > start_time:
                count += 1
        except OSError:
            continue
    return count


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    schema: list[dict[str, str]],
    required_inputs: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    product_status: dict[str, Any],
    r10_status: dict[str, Any],
    failure_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    source_ok = all(flag(row.get("exists", "")) and flag(row.get("needle_found", "")) for row in source_rows)
    add("V1060_1_sources_exist_and_needles", source_ok, "every cited source path exists and every source needle was found")
    schema_ok = len(schema) == len(PRODUCT_REQUIRED_COLUMNS)
    add("V1060_2_prediction_schema_written", schema_ok, "product prediction schema contains all required columns")
    required_ok = len(required_inputs) >= 4 and all(row.get("valid_for_claim") == "false" for row in required_inputs)
    add("V1060_3_required_inputs_written", required_ok, "required tau/source/KX inputs are explicit")
    template_nonclaim = prediction_rows and all(row.get("valid_for_claim") == "false" for row in prediction_rows)
    add("V1060_4_prediction_template_nonclaim", template_nonclaim, "prediction template rows are nonclaim placeholders")
    bounds_ok = any(row.get("bound_id") == "BOUND1060_0_clock_YbE3E2" and row.get("bound_value") == "2.1e-18" for row in bound_rows) and any(row.get("bound_id") == "BOUND1060_1_WEP_alpha" and row.get("bound_value") == "4.797780522732e-05" for row in bound_rows)
    add("V1060_5_bound_import_contains_clock_and_WEP", bounds_ok, "bound import includes clock and WEP product rows")
    product_refused = product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False
    add("V1060_6_product_runner_refuses_placeholders", product_refused, "custom alpha product runner refuses missing prediction rows")
    r10_refused = r10_status.get("valid_mts_rows") == 0 and r10_status.get("claim_allowed") is False
    add("V1060_7_R10_runner_refuses_placeholders", r10_refused, "existing R10 runner refuses placeholder rows")
    failures_ok = len(failure_rows) >= 3 and all(row.get("valid_for_claim") == "false" for row in failure_rows)
    add("V1060_8_failure_modes_written", failures_ok, "strict failure modes are written")
    claims_blocked = claim_rows and all(row.get("gate_pass") == "false" and row.get("claim_allowed") == "false" for row in claim_rows)
    add("V1060_9_claim_gates_blocked", claims_blocked, "all product test claim gates remain blocked")
    next_ok = bool(next_rows) and next_rows[0].get("next_target", "").startswith("1061-Y5-R10-WEP-alpha")
    add("V1060_10_next_target_written", next_ok, "next target row is present")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1060_11_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1060_12_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")

    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(0, {"check_id": "V1060_SUMMARY", "result": "pass" if summary_pass else "fail", "detail": "1060 alpha product prediction stub-runner validation summary", "generated_utc": stamp()})
    return checks


def write_doc(
    source_rows: list[dict[str, str]],
    schema: list[dict[str, str]],
    required_inputs: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    r10_status_rows_: list[dict[str, str]],
    failure_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1060 Y5 R10 alpha product prediction stub runner and required inputs",
            "",
            "**Progress:** the retained alpha branch now has a product-prediction runner schema. The runner has prediction rows, bound rows, validations, comparison output, and strict refusal modes.",
            "",
            "**Current verdict:** the runner correctly refuses all current MTS predictions because every prediction row still has missing tau/source/KX inputs. This is exactly the desired behaviour.",
            "",
            "**Next move:** fill the first WEP alpha product input set: `beta_source_alpha`, `tau_WEP`, and the material convention for `P_WEP_alpha`, or prove why it cannot be filled.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "",
            "## Product prediction schema",
            md_table(schema, ["column", "definition", "required", "valid_for_claim"]),
            "",
            "## Required inputs",
            md_table(required_inputs, ["input_id", "arena", "product_symbol", "required_numeric_inputs", "currently_available", "missing_status", "blocks"]),
            "",
            "## Prediction template",
            md_table(prediction_rows, ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "required_inputs", "derivation_status", "valid_for_claim"]),
            "",
            "## Bound import",
            md_table(bound_rows, ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "valid_for_claim"]),
            "",
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "",
            "## Product comparison rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "",
            "## R10 runner smoke status",
            md_table(r10_status_rows_, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
            "",
            "## Strict failure modes",
            md_table(failure_rows, ["failure_id", "object", "expected_failure", "observed_status", "meaning", "valid_for_claim"]),
            "",
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"]),
            "",
            "## Next target",
            md_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    schema = schema_rows()
    required_inputs = required_input_rows()
    prediction_rows = prediction_template_rows()
    bound_rows = bound_import_rows()
    claim_rows = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    mts_rows = mts_template_rows()

    outputs: dict[str, Path] = {
        "source_register": OUT / "P8_Y5_R10_1060_SOURCE_REGISTER.csv",
        "schema": OUT / "P8_Y5_R10_1060_PRODUCT_PREDICTION_SCHEMA.csv",
        "required_inputs": OUT / "P8_Y5_R10_1060_REQUIRED_INPUTS.csv",
        "prediction_template": PREDICTION_TEMPLATE,
        "bound_import": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1060_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1060_PRODUCT_COMPARISON_ROWS.csv",
        "r10_status": OUT / "P8_Y5_R10_1060_R10_RUNNER_SMOKE_STATUS.csv",
        "strict_failures": OUT / "P8_Y5_R10_1060_STRICT_FAILURE_MODES.csv",
        "claim_gates": OUT / "P8_Y5_R10_1060_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1060_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1060_NEXT_TARGET.csv",
        "mts_template": MTS_TEMPLATE,
        "validation": OUT / "P8_Y5_BRR545_1060_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["schema"], schema)
    write_csv(outputs["required_inputs"], required_inputs)
    write_csv(outputs["prediction_template"], prediction_rows, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound_import"], bound_rows, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)
    write_csv(outputs["mts_template"], mts_rows, MTS_REQUIRED_COLUMNS)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    r10_result = run_runner(MTS_TEMPLATE, BOUND_CANDIDATE, R10_RUN_DIR)
    r10_status = r10_result["status"]
    product_status_rows_ = product_runner_status_rows(product_status)
    r10_status_rows_ = r10_runner_status_rows(r10_status)
    failure_rows = strict_failure_rows(product_status, r10_status)
    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_result["comparisons"])
    write_csv(outputs["r10_status"], r10_status_rows_)
    write_csv(outputs["strict_failures"], failure_rows)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        schema,
        required_inputs,
        prediction_rows,
        bound_rows,
        product_status,
        r10_status,
        failure_rows,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        schema,
        required_inputs,
        prediction_rows,
        bound_rows,
        product_status_rows_,
        product_result["comparisons"],
        r10_status_rows_,
        failure_rows,
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
