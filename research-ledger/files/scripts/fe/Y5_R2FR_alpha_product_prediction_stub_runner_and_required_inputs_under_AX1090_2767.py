from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2767-Y5-R2FR-alpha-product-prediction-stub-runner-and-required-inputs-under-AX1090.md"
R10_SMOKE_DIR = MTS / "R10_runner_2767_alpha_product_refusal"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2767_SOURCE_REGISTER.csv",
    "schema": MTS / "P8_Y5_R2FR_2767_PRODUCT_PREDICTION_SCHEMA.csv",
    "required": MTS / "P8_Y5_R2FR_2767_REQUIRED_INPUTS.csv",
    "template": MTS / "P8_Y5_R2FR_2767_ALPHA_PRODUCT_PREDICTION_TEMPLATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2767_ALPHA_PRODUCT_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2767_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2767_PRODUCT_COMPARISON_ROWS.csv",
    "r10_template": MTS / "R10_alpha_lambda_curve_MTS_2767_ALPHA_PRODUCT_RUNNER_TEMPLATE_NONCLAIM.csv",
    "r10_smoke": MTS / "P8_Y5_R2FR_2767_R10_RUNNER_SMOKE_STATUS.csv",
    "failures": MTS / "P8_Y5_R2FR_2767_STRICT_FAILURE_MODES.csv",
    "gates": MTS / "P8_Y5_R2FR_2767_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2767_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2767_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2767_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2767_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "runner_queue": RAB_QUEUE / "JR2767_ALPHA_PRODUCT_PREDICTION_RUNNER_NONCLAIM.csv",
    "required_queue": RAB_QUEUE / "JR2767_ALPHA_PRODUCT_REQUIRED_INPUTS.csv",
    "beta_doc": BETA_DOCS / "ALPHA_PRODUCT_PREDICTION_RUNNER_2767_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "alpha_product_prediction_runner_2767_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2767_WEP_ALPHA_PRODUCT_INPUT_FILL_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent, R10_SMOKE_DIR}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(WORK))
    except ValueError:
        return str(path)


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    return {}


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2767_00_2766_next", "2766_next", MTS / "P8_Y5_R2FR_2766_NEXT_TARGET.csv", ["NEXT2766_0_2767"], "2766 handoff selecting alpha product-prediction runner"),
        ("SRC2767_01_2766_pack", "2766_product_pack", MTS / "P8_Y5_R2FR_2766_ALPHA_PRODUCT_PRIOR_PACK.csv", ["APP2766_2_WEP_alpha_Coulomb"], "R2/f(R) alpha product pack"),
        ("SRC2767_02_2766_transfer", "2766_transfer", MTS / "P8_Y5_R2FR_2766_NO_TRANSFER_GATES.csv", ["NTG2766_1_clock_to_WEP"], "R2/f(R) no-transfer gates"),
        ("SRC2767_03_2766_debts", "2766_debts", MTS / "P8_Y5_R2FR_2766_PROJECTION_DEBT_LEDGER.csv", ["PD2766_2_tau_WEP", "PD2766_5_visible_operator_universal_property"], "R2/f(R) projection debts"),
        ("SRC2767_04_1060_doc", "1060_doc", WORK / "1060-Y5-R10-alpha-product-prediction-stub-runner-and-required-inputs.md", ["PRED1060_1_WEP_alpha_template", "DEC1060_2_best_next"], "R10 product-runner precedent"),
        ("SRC2767_05_1060_schema", "1060_schema", MTS / "P8_Y5_R10_1060_PRODUCT_PREDICTION_SCHEMA.csv", ["prediction_id", "product_value"], "prior runner schema"),
        ("SRC2767_06_1060_required", "1060_required", MTS / "P8_Y5_R10_1060_REQUIRED_INPUTS.csv", ["REQ1060_1_WEP_alpha"], "prior required input list"),
        ("SRC2767_07_1060_status", "1060_status", MTS / "P8_Y5_R10_1060_PRODUCT_RUNNER_STATUS.csv", ["APR1060_0_alpha_product_stub"], "prior product runner refusal status"),
        ("SRC2767_08_1061_doc", "1061_doc", WORK / "1061-Y5-R10-WEP-alpha-product-first-input-fill-tauWEP-betaSource-material-map.md", ["DER1061_1_beta_source_alpha", "DER1061_2_tau_WEP"], "next WEP input-fill precedent"),
        ("SRC2767_09_r10_runner", "r10_runner", SCRIPTS / "R10_alpha_lambda_bound_prediction_runner.py", ["def run_runner", "valid_for_claim_not_true"], "existing R10 alpha(lambda) refusal runner"),
        ("SRC2767_10_r10_bound_candidate", "r10_bound_candidate", LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv", ["valid_for_claim"], "nonclaim R10 review-candidate bound curve"),
    ]
    rows = []
    for row_id, source_key, path, needles, role in specs:
        text = read_text(path)
        exists = path.exists()
        rows.append(nonclaim({
            "row_id": row_id,
            "source_key": source_key,
            "source_path": str(path),
            "exists": exists,
            "needle_spec": ";".join(needles),
            "needles_found": exists and all(needle in text for needle in needles),
            "source_role": role,
        }))
    return rows


def build_schema_rows() -> list[dict[str, Any]]:
    specs = [
        ("prediction_id", "stable row id", True),
        ("arena", "clock, MICROSCOPE_WEP, R10_short_range, or cross_arena", True),
        ("product_symbol", "exact product being predicted; runner may not algebraically split it", True),
        ("product_value", "numeric predicted product value only; no placeholders or derived-by-division values", True),
        ("product_units", "yr^-1, dimensionless, or dimensionless alpha(lambda) convention", True),
        ("product_source", "local source path for the prediction derivation", True),
        ("inputs_present", "semicolon-separated concrete input names that are numeric/sourced", True),
        ("required_inputs", "semicolon-separated input names required for this product", True),
        ("derivation_status", "DERIVED_NUMERIC, SYMBOLIC_ONLY, or MISSING_* status", True),
        ("comparison_allowed", "true only for rows with numeric product_value, source path, and all required inputs", True),
        ("valid_for_claim", "true only after all required inputs, numeric values, and source paths are real", True),
        ("notes", "nonclaim caveats and refusal reasons", True),
    ]
    return [nonclaim({"column": column, "definition": definition, "required": required}) for column, definition, required in specs]


def build_required_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "REQ2767_0_clock_product", "arena": "clock", "product_symbol": "P_clock_alpha", "required_numeric_inputs": "b_alpha_counterterm;tau_clock_time OR directly derived P_clock_alpha", "currently_available": "source-backed bound only, no MTS product prediction", "missing_status": "MISSING_MTS_PRODUCT_PREDICTION", "blocks": "clock product comparison as MTS prediction"}),
        nonclaim({"row_id": "REQ2767_1_WEP_alpha", "arena": "MICROSCOPE_WEP", "product_symbol": "P_WEP_alpha", "required_numeric_inputs": "beta_source_alpha;b_alpha_counterterm;tau_WEP OR directly derived P_WEP_alpha", "currently_available": "source-backed smoke target only", "missing_status": "MISSING_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT", "blocks": "WEP alpha product prediction"}),
        nonclaim({"row_id": "REQ2767_2_WEP_surface", "arena": "MICROSCOPE_WEP", "product_symbol": "P_WEP_surface", "required_numeric_inputs": "beta_source_or_binding;b_A;tau_WEP OR directly derived P_WEP_surface", "currently_available": "source-backed robust target only", "missing_status": "MISSING_BINDING_OWNER_AND_TAU_WEP", "blocks": "robust WEP product prediction"}),
        nonclaim({"row_id": "REQ2767_3_R10_alpha", "arena": "R10_short_range", "product_symbol": "P_R10_alpha(lambda)", "required_numeric_inputs": "lambda_X;Z_X;K_X^R10(lambda);beta_s(lambda);beta_t(lambda);tau_R10;epsilon_tail;promoted alpha_bound(lambda)", "currently_available": "schema plus review-candidate nonclaim bound curve", "missing_status": "MISSING_R10_FINITE_BRANCH_INPUTS", "blocks": "R10 alpha(lambda) product comparison"}),
        nonclaim({"row_id": "REQ2767_4_operator_domain", "arena": "cross_arena", "product_symbol": "alpha theorem-zero branch", "required_numeric_inputs": "derived visible operator-domain exhaustion OR retained finite product predictions", "currently_available": "exact contract, not theorem", "missing_status": "MISSING_VISIBLE_OPERATOR_UNIVERSAL_PROPERTY", "blocks": "standalone zero claim"}),
    ]


def build_prediction_template() -> list[dict[str, Any]]:
    return [
        nonclaim({"prediction_id": "PRED2767_0_clock_alpha_template", "arena": "clock", "product_symbol": "P_clock_alpha", "product_value": "MISSING_DERIVED_P_CLOCK_ALPHA", "product_units": "yr^-1", "product_source": "MISSING_SOURCE_FILE", "inputs_present": "none", "required_inputs": "b_alpha_counterterm;tau_clock_time OR directly derived P_clock_alpha", "derivation_status": "MISSING_MTS_PRODUCT_PREDICTION", "comparison_allowed": False, "notes": "clock bound exists but MTS product is not derived"}),
        nonclaim({"prediction_id": "PRED2767_1_WEP_alpha_template", "arena": "MICROSCOPE_WEP", "product_symbol": "P_WEP_alpha", "product_value": "MISSING_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT", "product_units": "dimensionless", "product_source": "MISSING_SOURCE_FILE", "inputs_present": "Delta_Q_alpha_abs;eta_bound;screened_product_target only", "required_inputs": "beta_source_alpha;b_alpha_counterterm;tau_WEP OR directly derived P_WEP_alpha", "derivation_status": "MISSING_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT", "comparison_allowed": False, "notes": "no beta_source_alpha=1, no tau_WEP=1, no clock-transfer shortcut"}),
        nonclaim({"prediction_id": "PRED2767_2_WEP_surface_template", "arena": "MICROSCOPE_WEP", "product_symbol": "P_WEP_surface", "product_value": "MISSING_BINDING_SOURCE_BA_TAU_WEP_PRODUCT", "product_units": "dimensionless", "product_source": "MISSING_SOURCE_FILE", "inputs_present": "surface/binding target only", "required_inputs": "beta_source_or_binding;b_A;tau_WEP OR directly derived P_WEP_surface", "derivation_status": "MISSING_BINDING_OWNER_AND_TAU_WEP", "comparison_allowed": False, "notes": "robust WEP branch retained as nonclaim"}),
        nonclaim({"prediction_id": "PRED2767_3_R10_alpha_template", "arena": "R10_short_range", "product_symbol": "P_R10_alpha(lambda)", "product_value": "MISSING_KX_BETA_SOURCE_BETA_TEST_TAU_R10_PRODUCT", "product_units": "dimensionless", "product_source": "MISSING_SOURCE_FILE", "inputs_present": "none", "required_inputs": "lambda_X;Z_X;K_X^R10(lambda);beta_s(lambda);beta_t(lambda);tau_R10;epsilon_tail", "derivation_status": "MISSING_R10_FINITE_BRANCH_INPUTS", "comparison_allowed": False, "notes": "R10 finite branch cannot score placeholders"}),
    ]


def build_bound_import() -> list[dict[str, Any]]:
    return [
        nonclaim({"bound_id": "BOUND2767_0_clock_YbE3E2", "arena": "clock", "product_symbol": "P_clock_alpha", "bound_value": "2.1e-18", "bound_units": "yr^-1", "bound_type": "upper_abs_1sigma_product_bound", "source_row": "APP2766_0_clock_YbE3E2"}),
        nonclaim({"bound_id": "BOUND2767_1_clock_AlHg", "arena": "clock", "product_symbol": "P_clock_alpha", "bound_value": "3.9e-17", "bound_units": "yr^-1", "bound_type": "weaker_upper_abs_1sigma_product_bound", "source_row": "APP2766_1_clock_AlHg"}),
        nonclaim({"bound_id": "BOUND2767_2_WEP_alpha", "arena": "MICROSCOPE_WEP", "product_symbol": "P_WEP_alpha", "bound_value": "4.797780522732e-05", "bound_units": "dimensionless", "bound_type": "required_abs_product_max_smoke_convention", "source_row": "APP2766_2_WEP_alpha_Coulomb"}),
        nonclaim({"bound_id": "BOUND2767_3_WEP_surface", "arena": "MICROSCOPE_WEP", "product_symbol": "P_WEP_surface", "bound_value": "2.887280314062e-05", "bound_units": "dimensionless", "bound_type": "required_abs_product_max_smoke_convention", "source_row": "APP2766_3_WEP_surface_binding"}),
        nonclaim({"bound_id": "BOUND2767_4_R10_alpha", "arena": "R10_short_range", "product_symbol": "P_R10_alpha(lambda)", "bound_value": "MISSING_PROMOTED_ALPHA_BOUND_CURVE", "bound_units": "dimensionless", "bound_type": "review_candidate_only", "source_row": "APP2766_4_R10_finite_alpha"}),
    ]


def is_numeric(value: Any) -> bool:
    try:
        float(str(value))
    except (TypeError, ValueError):
        return False
    return True


def has_missing_marker(row: dict[str, Any]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values())


def run_product_runner(predictions: list[dict[str, Any]], bounds: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    valid_predictions = [
        row for row in predictions
        if row.get("comparison_allowed") is True
        and row.get("valid_for_claim") is True
        and is_numeric(row.get("product_value"))
        and not has_missing_marker(row)
    ]
    valid_bounds = [
        row for row in bounds
        if is_numeric(row.get("bound_value"))
        and float(str(row.get("bound_value"))) > 0.0
        and not has_missing_marker(row)
    ]
    comparisons: list[dict[str, Any]] = []
    if not valid_predictions:
        comparisons.append(nonclaim({
            "comparison_id": "PRODUCT_COMPARE_NO_VALID_PREDICTIONS",
            "arena": "",
            "product_symbol": "",
            "product_value": "",
            "bound_value": "",
            "comparison_status": "not_run",
            "pass_for_claim": False,
            "issues": "no valid MTS alpha product prediction rows",
        }))
    else:
        for index, prediction in enumerate(valid_predictions):
            matching_bounds = [
                bound for bound in valid_bounds
                if bound.get("arena") == prediction.get("arena")
                and bound.get("product_symbol") == prediction.get("product_symbol")
            ]
            if not matching_bounds:
                comparisons.append(nonclaim({
                    "comparison_id": f"PRODUCT_COMPARE_{index}",
                    "arena": prediction.get("arena"),
                    "product_symbol": prediction.get("product_symbol"),
                    "product_value": prediction.get("product_value"),
                    "bound_value": "",
                    "comparison_status": "not_comparable",
                    "pass_for_claim": False,
                    "issues": "no matching numeric bound row",
                }))
                continue
            bound = matching_bounds[0]
            product_value = abs(float(str(prediction["product_value"])))
            bound_value = float(str(bound["bound_value"]))
            comparisons.append(nonclaim({
                "comparison_id": f"PRODUCT_COMPARE_{index}",
                "arena": prediction.get("arena"),
                "product_symbol": prediction.get("product_symbol"),
                "product_value": product_value,
                "bound_value": bound_value,
                "comparison_status": "pass" if product_value <= bound_value else "fail",
                "pass_for_claim": product_value <= bound_value,
                "issues": "" if product_value <= bound_value else "product_exceeds_bound",
            }))
    status = [
        nonclaim({
            "runner_id": "APR2767_0_alpha_product_stub",
            "prediction_rows": len(predictions),
            "bound_rows": len(bounds),
            "valid_prediction_rows": len(valid_predictions),
            "valid_bound_rows": len(valid_bounds),
            "comparison_rows": len(comparisons),
            "claim_allowed": False,
            "expected_result": "reject placeholder predictions and keep claim false",
        })
    ]
    return status, comparisons


def build_r10_template() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "model_id": "MTS_source_normalized_Newton_branch",
            "branch_id": "alpha_product_runner_template_2767",
            "curve_id": "R10_alpha_product_placeholder",
            "lambda_value": "MISSING_R10_LAMBDA_X",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_R10_PRODUCT_PREDICTION",
            "alpha_bound": "MISSING_PROMOTED_ALPHA_BOUND_CURVE",
            "alpha_bound_source": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "force_law_form": "P_R10_alpha(lambda)=K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)+epsilon_tail(lambda)",
            "derivation_status": "template_invalid_product_prior_pack_nonclaim",
            "formula_reference": "P8_Y5_R2FR_2767_REQUIRED_INPUTS.csv::REQ2767_3_R10_alpha",
            "source_file": "source-intake/mts_residuals/P8_Y5_R2FR_2767_ALPHA_PRODUCT_PREDICTION_TEMPLATE_NONCLAIM.csv",
            "assumptions": "no lambda_X/Z_X/K_X/tau_R10/beta_s/beta_t/effective bound promotion",
            "notes": "must be refused by R10 runner",
        })
    ]


def run_r10_smoke() -> list[dict[str, Any]]:
    sys.path.insert(0, str(SCRIPTS))
    from R10_alpha_lambda_bound_prediction_runner import run_runner

    result = run_runner(
        OUTPUTS["r10_template"],
        LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
        R10_SMOKE_DIR,
    )
    status = result["status"]
    return [
        nonclaim({
            "smoke_id": "SMOKE2767_0_R10_runner_refusal",
            "valid_mts_rows": status["valid_mts_rows"],
            "valid_bound_rows": status["valid_bound_rows"],
            "comparison_rows": status["comparison_rows"],
            "R10_pass_for_claim": status["R10_pass_for_claim"],
            "claim_allowed": status["claim_allowed"],
            "expected_result": "reject R10 alpha product placeholders until prediction inputs are sourced",
            "output_dir": status["output_dir"],
        })
    ]


def build_failures(runner_status: list[dict[str, Any]], r10_status: list[dict[str, Any]]) -> list[dict[str, Any]]:
    valid_predictions = runner_status[0]["valid_prediction_rows"]
    return [
        nonclaim({"row_id": "SFR2767_0_missing_product_predictions", "object": "alpha product prediction template", "expected_failure": "valid_prediction_rows=0", "observed_status": f"valid_prediction_rows={valid_predictions}", "meaning": "runner refuses missing tau/source/KX placeholder rows"}),
        nonclaim({"row_id": "SFR2767_1_no_standalone_claim", "object": "standalone b_alpha or beta_source_alpha", "expected_failure": "not represented as scoreable products", "observed_status": "standalone claims absent from prediction schema", "meaning": "runner cannot divide by guessed tau/source factors"}),
        nonclaim({"row_id": "SFR2767_2_no_unity_shortcuts", "object": "tau_clock;tau_WEP;tau_R10;beta_source_alpha", "expected_failure": "no variable set to 1 by convention", "observed_status": "all unity shortcuts absent", "meaning": "coupling must come from theory or stay nonclaim"}),
        nonclaim({"row_id": "SFR2767_3_R10_runner", "object": "R10 alpha(lambda) smoke row", "expected_failure": "valid_mts_rows=0", "observed_status": f"valid_mts_rows={r10_status[0]['valid_mts_rows']}; valid_bound_rows={r10_status[0]['valid_bound_rows']}", "meaning": "existing R10 runner refuses finite-branch placeholders"}),
    ]


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CG2767_0_product_runner_claim", "claim": "alpha product runner has scoreable MTS predictions", "gate_pass": False, "reason": "prediction template contains missing tau/source/KX inputs", "claim_allowed": False}),
        nonclaim({"row_id": "CG2767_1_clock", "claim": "clock product prediction is tested", "gate_pass": False, "reason": "source-backed clock bound exists but MTS P_clock_alpha prediction is missing", "claim_allowed": False}),
        nonclaim({"row_id": "CG2767_2_WEP", "claim": "WEP alpha product prediction is tested", "gate_pass": False, "reason": "P_WEP_alpha prediction and tau_WEP/beta_source/b_alpha product are missing", "claim_allowed": False}),
        nonclaim({"row_id": "CG2767_3_R10", "claim": "R10 alpha(lambda) product prediction is tested", "gate_pass": False, "reason": "R10 finite branch inputs and promoted bound curve are missing", "claim_allowed": False}),
        nonclaim({"row_id": "CG2767_4_local_GR", "claim": "local GR/Newton follows from alpha product runner", "gate_pass": False, "reason": "runner is a refusal guardrail, not a derivation of the local constant sector", "claim_allowed": False}),
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "DEC2767_0_runner_built", "decision": "alpha product-prediction runner schema now exists in the current R2/f(R) branch", "because": "2766 retained the alpha counterterm/product-prior branch and forbade transfer shortcuts", "next_action": "fill one product prediction input set rather than claiming from bounds alone"}),
        nonclaim({"row_id": "DEC2767_1_runner_refuses", "decision": "runner correctly refuses all current MTS placeholder predictions", "because": "valid prediction rows are zero and missing markers remain", "next_action": "derive or source tau_WEP/beta_source_alpha/b_alpha product first"}),
        nonclaim({"row_id": "DEC2767_2_best_next", "decision": "next target is the first WEP alpha product input fill in the R2/f(R) branch", "because": "WEP has the clearest numeric product target and the missing inputs are explicitly named", "next_action": "2768-Y5-R2FR-WEP-alpha-product-first-input-fill-tauWEP-betaSource-material-map-under-AX1090.md"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2767_0_2768",
            "next_target": "2768-Y5-R2FR-WEP-alpha-product-first-input-fill-tauWEP-betaSource-material-map-under-AX1090.md",
            "script": "scripts/Y5_R2FR_WEP_alpha_product_first_input_fill_tauWEP_betaSource_material_map_under_AX1090_2768.py",
            "why": "the runner now blocks all placeholder alpha products; the least handwavy next step is to fill or reject the WEP product inputs beta_source_alpha, b_alpha/tau product, tau_WEP, and material convention in one parent/source map",
            "include": "tau_WEP definition source, beta_source_alpha owner route, WEP material convention, direct P_WEP_alpha theorem route, strict failure if any input is missing",
            "exclude": "standalone b_alpha claim, guessed tau values, beta_source_alpha=1, tau_WEP=1, cancellation, public WEP/R10/clock/local-GR claim, GitHub, formalization-workbench edits",
        })
    ]


def copy_branch_outputs(
    required: list[dict[str, Any]],
    template: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    comparisons: list[dict[str, Any]],
    failures: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    runner_rows = template + runner + comparisons + failures + gates
    microscope_rows = [row for row in required + template if "WEP" in str(row.get("arena", ""))] + comparisons + gates + next_rows
    beta_rows = required + template + failures + next_rows
    specs = [
        ("BR2767_0_runner_queue", "runner", runner_rows, OUTPUTS["runner"], BRANCH_OUTPUTS["runner_queue"], "alpha product-prediction refusal runner"),
        ("BR2767_1_required_queue", "required", required, OUTPUTS["required"], BRANCH_OUTPUTS["required_queue"], "required tau/source/KX input list"),
        ("BR2767_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["required"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing required-input copy"),
        ("BR2767_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["template"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE WEP product runner copy"),
        ("BR2767_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next WEP alpha input-fill target"),
    ]
    rows = []
    for copy_id, table_key, source_rows, source_table, copy_path, purpose in specs:
        write_csv(copy_path, source_rows)
        rows.append(nonclaim({
            "copy_id": copy_id,
            "table_key": table_key,
            "source_table": rel(source_table),
            "copy_path": rel(copy_path),
            "purpose": purpose,
            "exists": copy_path.exists(),
            "row_count": csv_row_count(copy_path) if copy_path.exists() else 0,
        }))
    return rows


def generated_files_under_work() -> bool:
    generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    generated += [path for path in R10_SMOKE_DIR.rglob("*") if path.is_file()]
    return all(WORK in path.parents or path == WORK for path in generated)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime > RUN_STARTED_UTC.timestamp():
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("valid_for_claim", "False")).lower() == "true":
                return False
            if str(row.get("claim_allowed", "False")).lower() == "true":
                return False
            if str(row.get("allowed", "False")).lower() == "true":
                return False
            if str(row.get("pass_for_claim", "False")).lower() == "true":
                return False
    return True


def remove_pycache() -> None:
    pycache = SCRIPTS / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    schema = rows_by_name["schema"]
    required = rows_by_name["required"]
    template = rows_by_name["template"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    comparisons = rows_by_name["comparisons"]
    r10_smoke = rows_by_name["r10_smoke"]
    failures = rows_by_name["failures"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    required_columns = {"prediction_id", "arena", "product_symbol", "product_value", "product_units", "product_source", "inputs_present", "required_inputs", "derivation_status", "comparison_allowed", "valid_for_claim"}
    schema_columns = {row["column"] for row in schema}
    checks = [
        ("VAL2767_0_sources", all(row["exists"] and row["needles_found"] for row in sources), "every cited source path exists and needles are found"),
        ("VAL2767_1_prediction_schema_written", required_columns.issubset(schema_columns), "product prediction schema contains all required columns"),
        ("VAL2767_2_required_inputs_written", all(any(row["row_id"] == required_id for row in required) for required_id in ["REQ2767_0_clock_product", "REQ2767_1_WEP_alpha", "REQ2767_3_R10_alpha"]), "required tau/source/KX inputs are explicit"),
        ("VAL2767_3_prediction_template_nonclaim", all(row["valid_for_claim"] is False and row["comparison_allowed"] is False and has_missing_marker(row) for row in template), "prediction template rows are nonclaim placeholders"),
        ("VAL2767_4_bound_import_contains_clock_WEP", all(any(row["row_id"] == required_id if "row_id" in row else row["bound_id"] == required_id for row in bounds) for required_id in ["BOUND2767_0_clock_YbE3E2", "BOUND2767_2_WEP_alpha"]), "bound import includes clock and WEP product rows"),
        ("VAL2767_5_product_runner_refuses_placeholders", runner[0]["valid_prediction_rows"] == 0 and runner[0]["claim_allowed"] is False and comparisons[0]["comparison_status"] == "not_run", "custom alpha product runner refuses missing prediction rows"),
        ("VAL2767_6_R10_runner_refuses_placeholders", r10_smoke[0]["valid_mts_rows"] == 0 and r10_smoke[0]["claim_allowed"] is False, "existing R10 runner refuses placeholder rows"),
        ("VAL2767_7_failure_modes_written", all(any(row["row_id"] == required_id for row in failures) for required_id in ["SFR2767_0_missing_product_predictions", "SFR2767_2_no_unity_shortcuts", "SFR2767_3_R10_runner"]), "strict failure modes are written"),
        ("VAL2767_8_claim_gates_blocked", all(row["gate_pass"] is False and row["claim_allowed"] is False for row in gates), "all product test claim gates remain blocked"),
        ("VAL2767_9_next_target_written", any(row["row_id"] == "NEXT2767_0_2768" and "WEP-alpha-product-first-input-fill" in row["next_target"] for row in next_rows), "next target row is present"),
        ("VAL2767_10_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2767_11_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2767_12_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/allowed=true/pass_for_claim=true"),
        ("VAL2767_13_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2767_14_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2767_15_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2767_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2767 builds the current R2/f(R) alpha product-prediction refusal runner, imports clock/WEP/R10 product bounds, confirms all MTS prediction rows are placeholders with missing tau/source/KX inputs, verifies the R10 runner also refuses the placeholder alpha(lambda) curve, keeps all claim gates blocked, and selects WEP alpha product input fill as the next target.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2767 - Y5 R2/f(R): Alpha Product-Prediction Stub Runner And Required Inputs Under AX1090",
        "## Private Verdict\n\nThe runner is now in place for the current R2/f(R) branch. It does exactly what we want: it refuses to score alpha/coupling products while `tau_clock`, `tau_WEP`, `tau_R10`, `beta_source_alpha`, `K_X/Z_X`, and direct product derivations are missing.\n\nThis is not a physics pass. It is a guardrail against accidentally winning by notation. The next real move is to try to fill the WEP alpha product input set, because that is the nearest concrete lab arena with a numerical product target.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "## Product Prediction Schema\n\n" + markdown_table(rows_by_name["schema"], ["column", "definition", "required", "valid_for_claim"]),
        "## Required Inputs\n\n" + markdown_table(rows_by_name["required"], ["row_id", "arena", "product_symbol", "required_numeric_inputs", "currently_available", "missing_status", "blocks", "valid_for_claim"]),
        "## Prediction Template\n\n" + markdown_table(rows_by_name["template"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "required_inputs", "derivation_status", "comparison_allowed", "valid_for_claim"]),
        "## Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "source_row", "valid_for_claim"]),
        "## Product Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result", "valid_for_claim"]),
        "## Product Comparison Rows\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## R10 Runner Smoke Status\n\n" + markdown_table(rows_by_name["r10_smoke"], ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result", "output_dir", "valid_for_claim"]),
        "## Strict Failure Modes\n\n" + markdown_table(rows_by_name["failures"], ["row_id", "object", "expected_failure", "observed_status", "meaning", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["row_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decision"], ["row_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "why", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis checkpoint is the referee. If the theory cannot produce the coupling product, the code now says no. That is good discipline: before we try to beat GR/DM/MOND in a lab arena, we first force MTS to speak in the exact product the lab actually constrains.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    schema = build_schema_rows()
    required = build_required_rows()
    template = build_prediction_template()
    bounds = build_bound_import()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["schema"], schema)
    write_csv(OUTPUTS["required"], required)
    write_csv(OUTPUTS["template"], template)
    write_csv(OUTPUTS["bounds"], bounds)

    runner, comparisons = run_product_runner(template, bounds)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["comparisons"], comparisons)

    r10_template = build_r10_template()
    write_csv(OUTPUTS["r10_template"], r10_template)
    r10_smoke = run_r10_smoke()
    write_csv(OUTPUTS["r10_smoke"], r10_smoke)

    failures = build_failures(runner, r10_smoke)
    gates = build_gates()
    decision = build_decision()
    next_rows = build_next()

    write_csv(OUTPUTS["failures"], failures)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_rows)

    branches = copy_branch_outputs(required, template, runner, comparisons, failures, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "schema": schema,
        "required": required,
        "template": template,
        "bounds": bounds,
        "runner": runner,
        "comparisons": comparisons,
        "r10_template": r10_template,
        "r10_smoke": r10_smoke,
        "failures": failures,
        "gates": gates,
        "decision": decision,
        "next": next_rows,
        "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    csv_paths += [path for path in R10_SMOKE_DIR.rglob("*.csv")]
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2767_OVERALL")
    print(f"2767 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
