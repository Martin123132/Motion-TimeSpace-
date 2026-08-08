from __future__ import annotations

import csv
import shutil
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
DOC = WORK / "2768-Y5-R2FR-WEP-alpha-product-first-input-fill-tauWEP-betaSource-material-map-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2768_SOURCE_REGISTER.csv",
    "material": MTS / "P8_Y5_R2FR_2768_WEP_MATERIAL_CONVENTION.csv",
    "derivation": MTS / "P8_Y5_R2FR_2768_BETA_TAU_DERIVATION_ATTEMPT.csv",
    "inputs": MTS / "P8_Y5_R2FR_2768_INPUT_FILL_LEDGER.csv",
    "prediction": MTS / "P8_Y5_R2FR_2768_ALPHA_PRODUCT_PREDICTION_ATTEMPT_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2768_ALPHA_PRODUCT_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2768_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2768_PRODUCT_COMPARISON_ROWS.csv",
    "failures": MTS / "P8_Y5_R2FR_2768_STRICT_FAILURE_MODES.csv",
    "gates": MTS / "P8_Y5_R2FR_2768_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2768_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2768_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2768_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2768_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "wep_queue": RAB_QUEUE / "JR2768_WEP_ALPHA_PRODUCT_INPUT_FILL_NONCLAIM.csv",
    "material_queue": RAB_QUEUE / "JR2768_WEP_MATERIAL_CONVENTION_SMOKE_ONLY.csv",
    "beta_doc": BETA_DOCS / "WEP_ALPHA_PRODUCT_INPUT_FILL_2768_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "wep_alpha_product_input_fill_2768_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2768_PARENT_WEP_PRODUCT_THEOREM_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
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
        ("SRC2768_00_2767_next", "2767_next", MTS / "P8_Y5_R2FR_2767_NEXT_TARGET.csv", ["NEXT2767_0_2768"], "2767 handoff selecting WEP input fill"),
        ("SRC2768_01_2767_required", "2767_required", MTS / "P8_Y5_R2FR_2767_REQUIRED_INPUTS.csv", ["REQ2767_1_WEP_alpha"], "R2/f(R) WEP required inputs"),
        ("SRC2768_02_2767_prediction", "2767_prediction_template", MTS / "P8_Y5_R2FR_2767_ALPHA_PRODUCT_PREDICTION_TEMPLATE_NONCLAIM.csv", ["PRED2767_1_WEP_alpha_template"], "R2/f(R) WEP placeholder prediction"),
        ("SRC2768_03_2767_bound", "2767_bound", MTS / "P8_Y5_R2FR_2767_ALPHA_PRODUCT_BOUND_IMPORT.csv", ["BOUND2767_2_WEP_alpha"], "R2/f(R) WEP product target"),
        ("SRC2768_04_2767_runner", "2767_runner", MTS / "P8_Y5_R2FR_2767_PRODUCT_RUNNER_STATUS.csv", ["APR2767_0_alpha_product_stub"], "R2/f(R) runner refusal status"),
        ("SRC2768_05_1061_doc", "1061_doc", WORK / "1061-Y5-R10-WEP-alpha-product-first-input-fill-tauWEP-betaSource-material-map.md", ["DER1061_1_beta_source_alpha", "DER1061_2_tau_WEP"], "prior WEP input-fill precedent"),
        ("SRC2768_06_650_screen_rule", "650_screen_rule", MTS / "P8_Y5_R10_650_ULTRA_SCREENED_RULE.csv", ["USR650_0_shared_screen_variable"], "shared screen convention"),
        ("SRC2768_07_650_cross_arena", "650_cross_arena", MTS / "P8_Y5_R10_650_CROSS_ARENA_CONTRACT.csv", ["R0_R1_WEP"], "cross-arena WEP contract"),
        ("SRC2768_08_651_stress", "651_stress", MTS / "P8_Y5_R10_651_WEP_ALPHA_STRESS_TEST.csv", ["WAS651_0_alpha_Coulomb"], "WEP alpha stress row"),
        ("SRC2768_09_983_web", "983_web", MTS / "P8_Y5_R10_983_WEB_SOURCE_REGISTER.csv", ["WEB983_0_MICROSCOPE_CQG_COMPOSITION"], "MICROSCOPE composition source register"),
        ("SRC2768_10_983_delta", "983_delta", MTS / "P8_Y5_R10_983_DIFFERENTIAL_PROXY_VECTOR.csv", ["DEL983_coulomb_proxy"], "differential material proxy"),
        ("SRC2768_11_1053_matrix", "1053_matrix", MTS / "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv", ["WCM1053_4"], "WEP composition charge matrix"),
        ("SRC2768_12_988_pressure", "988_pressure", MTS / "P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv", ["WEP988_WAS651_0_alpha_Coulomb"], "WEP alpha pressure import"),
        ("SRC2768_13_1052_WEP", "1052_WEP", MTS / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv", ["AWP1052_0_alpha_Coulomb"], "alpha WEP projection ledger"),
        ("SRC2768_14_1053_beta", "1053_beta", MTS / "P8_Y5_R10_1053_BETA_SOURCE_ALPHA_DERIVATION_AUDIT.csv", ["BSA1053_1_alpha_marker_source"], "beta_source_alpha derivation audit"),
        ("SRC2768_15_1053_tau", "1053_tau", MTS / "P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv", ["TPR1053_1_tau_WEP_definition"], "tau_WEP derivation audit"),
        ("SRC2768_16_989_owner", "989_owner", MTS / "P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv", ["BSO989_0_definition"], "beta source owner ledger"),
        ("SRC2768_17_990_contract", "990_contract", MTS / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv", ["PAC990_3_EM_lock"], "EM/current parent action contract"),
        ("SRC2768_18_local_bound", "local_bound", LOCAL_BOUNDS / "local_bound_claims.csv", ["R1_WEP_source_charge"], "local WEP source-charge bound"),
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


def load_inputs() -> dict[str, dict[str, str]]:
    return {
        "matrix": find_row(read_csv_rows(MTS / "P8_Y5_R10_1053_WEP_COMPOSITION_CHARGE_MATRIX.csv"), "row_id", "WCM1053_4"),
        "pressure": find_row(read_csv_rows(MTS / "P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv"), "row_id", "WEP988_WAS651_0_alpha_Coulomb"),
        "wep_ledger": find_row(read_csv_rows(MTS / "P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv"), "projection_id", "AWP1052_0_alpha_Coulomb"),
        "beta": find_row(read_csv_rows(MTS / "P8_Y5_R10_1053_BETA_SOURCE_ALPHA_DERIVATION_AUDIT.csv"), "audit_id", "BSA1053_1_alpha_marker_source"),
        "tau": find_row(read_csv_rows(MTS / "P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv"), "tau_id", "TPR1053_1_tau_WEP_definition"),
        "owner": find_row(read_csv_rows(MTS / "P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv"), "owner_id", "BSO989_0_definition"),
        "bound": find_row(read_csv_rows(MTS / "P8_Y5_R2FR_2767_ALPHA_PRODUCT_BOUND_IMPORT.csv"), "bound_id", "BOUND2767_2_WEP_alpha"),
    }


def build_material_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "MCON2768_0_test_pair", "object": "MICROSCOPE Ti/Pt test-pair convention", "definition": "TA6V outer test mass minus PtRh10 inner test mass; eta_AB uses the same sign convention as the 983/1053 smoke rows.", "numeric_value": "not_applicable", "units": "dimensionless", "source_row": "WEB983_0_MICROSCOPE_CQG_COMPOSITION; WCM1053_4", "status": "material_pair_convention_filled_for_smoke", "blocks_claim": "full material tensor and parent source/readout convention still missing"}),
        nonclaim({"row_id": "MCON2768_1_delta_Q_alpha", "object": "Delta_Q_alpha_Coulomb_abs", "definition": "absolute alpha/Coulomb differential material charge in the Damour-Donoghue smoke convention.", "numeric_value": inputs["matrix"].get("Delta_Q_alpha_abs", "0.001989808886825"), "units": "dimensionless", "source_row": "WCM1053_4", "status": "numeric_smoke_delta_filled", "blocks_claim": "source-backed smoke estimate, not full MICROSCOPE material tensor"}),
        nonclaim({"row_id": "MCON2768_2_eta_bound", "object": "eta_WEP_source_charge_bound", "definition": "MICROSCOPE Ti/Pt upper bound imported as the WEP product target anchor.", "numeric_value": "2.800000e-15", "units": "dimensionless", "source_row": "R1_WEP_source_charge; WEP988_WAS651_0_alpha_Coulomb", "status": "numeric_bound_anchor_filled", "blocks_claim": "bound alone is not an MTS prediction"}),
        nonclaim({"row_id": "MCON2768_3_screened_product_target", "object": "abs_P_WEP_alpha_target", "definition": "under the 650/651 shared-screen smoke convention, |P_WEP_alpha| <= eta_bound/unit_source_eta_prediction.", "numeric_value": inputs["bound"].get("bound_value", "4.797780522732e-05"), "units": "dimensionless", "source_row": "WEP988_WAS651_0_alpha_Coulomb; AWP1052_0_alpha_Coulomb; BOUND2767_2_WEP_alpha", "status": "score_threshold_filled_not_prediction", "blocks_claim": "P_WEP_alpha itself still requires beta_source_alpha, b_alpha, and tau_WEP or a direct parent product derivation"}),
    ]


def build_derivation_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "DER2768_0_product_definition", "target": "P_WEP_alpha", "attempted_derivation": "P_WEP_alpha := beta_source_alpha*b_alpha*tau_WEP, or directly as the parent variation of the alpha-sensitive source/test acceleration map.", "available_evidence": "material delta and screened product target are numeric in the 650/651/988/1052/2767 smoke convention", "missing_premise": "parent source-normalization functional, alpha-counterterm owner, and WEP orbit/source projection", "result": "PRODUCT_CONTRACT_WRITTEN_NOT_DERIVED", "next_action": "derive the combined product from parent matter/source action instead of assigning beta_source_alpha=1 or tau_WEP=1"}),
        nonclaim({"row_id": "DER2768_1_beta_source_alpha", "target": "beta_source_alpha", "attempted_derivation": inputs["beta"].get("formula", "beta_source_alpha as alpha-channel source/force normalization"), "available_evidence": "BSA1053_1 and BSO989_0 define the required owner", "missing_premise": inputs["beta"].get("missing_for_claim", "parent matter functional, Noether current normalization, and no-marker/no-alpha theorem are unsigned"), "result": inputs["beta"].get("derivation_status", "OWNER_NOT_DERIVED"), "next_action": "hunt parent source-normalization owner or prove beta_source_alpha=0 by EM-lock/no-alpha theorem"}),
        nonclaim({"row_id": "DER2768_2_tau_WEP", "target": "tau_WEP", "attempted_derivation": inputs["tau"].get("definition_or_formula", "tau_WEP as normalized lab/source/orbit projection"), "available_evidence": "TPR1053_1 defines the object; 650 requires the shared local alpha screen across clocks/WEP/R10", "missing_premise": inputs["tau"].get("missing_for_claim", "Earth/source worldtube, spacecraft/environment averaging, material tensor, parent Xhat normalization, and observed-force readout"), "result": inputs["tau"].get("current_status", "PROJECTION_NOT_DERIVED"), "next_action": "derive tau_WEP from local source geometry or replace split beta*tau by a direct P_WEP_alpha theorem"}),
        nonclaim({"row_id": "DER2768_3_balpha_or_direct_product", "target": "b_alpha_counterterm or direct P_WEP_alpha", "attempted_derivation": "use retained alpha counterterm branch only as an exact product, never as standalone b_alpha divided from clock bounds", "available_evidence": "2766/2767 retain product-prior branch and block transfer shortcuts", "missing_premise": "visible operator-domain exhaustion or numeric direct product prediction from parent action", "result": "DIRECT_PRODUCT_NOT_DERIVED", "next_action": "try parent WEP product theorem; otherwise demote WEP alpha route to closure-only"}),
        nonclaim({"row_id": "DER2768_4_material_convention", "target": "MICROSCOPE alpha material map", "attempted_derivation": "use existing PtRh10/TA6V smoke alloy map and Delta_Q_alpha_Coulomb as the first product convention.", "available_evidence": "WEB983_0, WCM1053_4, WEP988_WAS651_0, AWP1052_0, and BOUND2767_2", "missing_premise": "full material tensor and source/readout convention for a claim-grade MICROSCOPE prediction", "result": "PARTIAL_FILLED_SMOKE_CONVENTION_ONLY", "next_action": "use this as the first internal scoring convention, not public evidence"}),
    ]


def build_input_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "INF2768_0_material_pair", "required_input": "MICROSCOPE material convention", "value_or_status": "TA6V_minus_PtRh10", "source": "WEB983_0_MICROSCOPE_CQG_COMPOSITION; WCM1053_4", "filled_status": "filled_for_smoke_only", "why_not_claim": "full material/source/readout tensor missing"}),
        nonclaim({"row_id": "INF2768_1_delta_Q_alpha", "required_input": "Delta_Q_alpha_Coulomb_abs", "value_or_status": inputs["matrix"].get("Delta_Q_alpha_abs", "0.001989808886825"), "source": "WCM1053_4; AWP1052_0_alpha_Coulomb", "filled_status": "filled_for_smoke_only", "why_not_claim": "smoke formula, not complete material model"}),
        nonclaim({"row_id": "INF2768_2_product_bound", "required_input": "abs_P_WEP_alpha_bound", "value_or_status": inputs["bound"].get("bound_value", "4.797780522732e-05"), "source": "WEP988_WAS651_0_alpha_Coulomb; BOUND2767_2_WEP_alpha", "filled_status": "target_filled_not_prediction", "why_not_claim": "a bound threshold is not an MTS-predicted product"}),
        nonclaim({"row_id": "INF2768_3_beta_source_alpha", "required_input": "beta_source_alpha", "value_or_status": "MISSING_PARENT_SOURCE_NORMALIZATION_OWNER", "source": "BSA1053_1_alpha_marker_source; BSO989_0_definition", "filled_status": "not_filled", "why_not_claim": "cannot set source normalization to unity; needs parent matter/Noether source owner or zero theorem"}),
        nonclaim({"row_id": "INF2768_4_tau_WEP", "required_input": "tau_WEP", "value_or_status": "MISSING_LAB_SOURCE_ORBIT_PROJECTION", "source": "TPR1053_1_tau_WEP_definition; PR650_1_WEP", "filled_status": "not_filled", "why_not_claim": "cannot set tau_WEP to one; needs local geometry/source profile/readout map"}),
        nonclaim({"row_id": "INF2768_5_b_alpha_or_direct_product", "required_input": "b_alpha_counterterm or direct P_WEP_alpha", "value_or_status": "MISSING_PARENT_ALPHA_COUNTERTERM_PRODUCT", "source": "PRED2767_1_WEP_alpha_template; ACP2766_5_R2FR_policy", "filled_status": "not_filled", "why_not_claim": "standalone b_alpha remains forbidden; only a directly derived product may be scored"}),
    ]


def build_prediction_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2768_0_WEP_alpha_material_convention_filled",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha",
            "product_value": "MISSING_PARENT_DERIVED_BETA_SOURCE_ALPHA_B_ALPHA_TAU_WEP_PRODUCT",
            "product_units": "dimensionless",
            "inputs_present": "Delta_Q_alpha_abs;eta_bound;screened_product_target",
            "required_inputs": "beta_source_alpha;b_alpha_counterterm;tau_WEP OR directly derived P_WEP_alpha",
            "derivation_status": "MATERIAL_CONVENTION_FILLED_BETA_TAU_PRODUCT_MISSING",
            "comparison_allowed": False,
            "claim_allowed": False,
        })
    ]


def build_bound_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    return [
        nonclaim({"bound_id": "BOUND2768_0_WEP_alpha_screened_product_target", "arena": "MICROSCOPE_WEP", "product_symbol": "P_WEP_alpha", "bound_value": inputs["bound"].get("bound_value", "4.797780522732e-05"), "bound_units": "dimensionless", "bound_source": "source-intake/mts_residuals/P8_Y5_R2FR_2767_ALPHA_PRODUCT_BOUND_IMPORT.csv", "source_row": "BOUND2767_2_WEP_alpha", "bound_type": "screened_smoke_product_target_nonclaim", "notes": "Internal target only: uses 650/651 shared-screen smoke convention and cannot become a claim without a real MTS product prediction."})
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
        and row.get("claim_allowed") is True
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
    if not valid_predictions:
        comparisons = [nonclaim({
            "comparison_id": "PRODUCT_COMPARE_NO_VALID_PREDICTIONS",
            "arena": "",
            "product_symbol": "",
            "product_value": "",
            "bound_value": "",
            "comparison_status": "not_run",
            "pass_for_claim": False,
            "issues": "no valid MTS alpha product prediction rows",
        })]
    else:
        comparisons = []
        for index, prediction in enumerate(valid_predictions):
            matching_bounds = [
                bound for bound in valid_bounds
                if bound.get("arena") == prediction.get("arena")
                and bound.get("product_symbol") == prediction.get("product_symbol")
            ]
            if not matching_bounds:
                comparisons.append(nonclaim({"comparison_id": f"PRODUCT_COMPARE_{index}", "arena": prediction.get("arena"), "product_symbol": prediction.get("product_symbol"), "product_value": prediction.get("product_value"), "bound_value": "", "comparison_status": "not_comparable", "pass_for_claim": False, "issues": "no matching numeric bound"}))
                continue
            bound_value = float(str(matching_bounds[0]["bound_value"]))
            product_value = abs(float(str(prediction["product_value"])))
            comparisons.append(nonclaim({"comparison_id": f"PRODUCT_COMPARE_{index}", "arena": prediction.get("arena"), "product_symbol": prediction.get("product_symbol"), "product_value": product_value, "bound_value": bound_value, "comparison_status": "pass" if product_value <= bound_value else "fail", "pass_for_claim": product_value <= bound_value, "issues": "" if product_value <= bound_value else "product_exceeds_bound"}))
    runner = [nonclaim({
        "runner_id": "APR2768_0_WEP_alpha_product_attempt",
        "prediction_rows": len(predictions),
        "bound_rows": len(bounds),
        "valid_prediction_rows": len(valid_predictions),
        "valid_bound_rows": len(valid_bounds),
        "comparison_rows": len(comparisons),
        "claim_allowed": False,
        "expected_result": "reject_missing_parent_product",
    })]
    return runner, comparisons


def build_failures() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "FAIL2768_0_no_beta_source_owner", "object": "beta_source_alpha", "expected_failure": "MISSING_PARENT_SOURCE_NORMALIZATION_OWNER", "observed_status": "not_filled", "meaning": "WEP alpha product cannot be predicted from a source/test coupling until the parent matter/Noether owner is signed."}),
        nonclaim({"row_id": "FAIL2768_1_no_tau_WEP_projection", "object": "tau_WEP", "expected_failure": "MISSING_LAB_SOURCE_ORBIT_PROJECTION", "observed_status": "not_filled", "meaning": "The shared screen cannot be exported into WEP acceleration without a source geometry/readout projection."}),
        nonclaim({"row_id": "FAIL2768_2_no_direct_product", "object": "P_WEP_alpha", "expected_failure": "MISSING_PARENT_ALPHA_COUNTERTERM_PRODUCT", "observed_status": "not_filled", "meaning": "The observable product itself is not derived; the target bound is only a target."}),
        nonclaim({"row_id": "FAIL2768_3_no_unity_shortcuts", "object": "beta_source_alpha;tau_WEP", "expected_failure": "no beta=1 or tau=1 replacement", "observed_status": "unity shortcuts absent", "meaning": "No coefficient is promoted by convention; the coupling must come from the theory."}),
    ]


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CG2768_0_material_convention_claim", "claim": "MICROSCOPE material convention is claim-grade", "gate_pass": False, "reason": "only a smoke alloy/material charge convention is filled; full tensor/readout source map is missing", "claim_allowed": False}),
        nonclaim({"row_id": "CG2768_1_beta_source_alpha_claim", "claim": "beta_source_alpha is derived or bounded by MTS", "gate_pass": False, "reason": "owner ledger still says source normalization is unowned", "claim_allowed": False}),
        nonclaim({"row_id": "CG2768_2_tau_WEP_claim", "claim": "tau_WEP is derived", "gate_pass": False, "reason": "tau_WEP remains a definition requiring lab/source/orbit projection", "claim_allowed": False}),
        nonclaim({"row_id": "CG2768_3_WEP_alpha_product_pass", "claim": "MTS passes WEP alpha/Coulomb product target", "gate_pass": False, "reason": "product target exists but no numeric MTS product prediction exists", "claim_allowed": False}),
        nonclaim({"row_id": "CG2768_4_local_GR", "claim": "local GR/Newton follows from WEP alpha input fill", "gate_pass": False, "reason": "input fill does not close the parent action, EM owner, source functor, or PPN residual", "claim_allowed": False}),
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "DEC2768_0_material_convention", "decision": "keep the MICROSCOPE alpha material convention as an internal smoke target only", "because": "Delta_Q_alpha and the screened product target are numeric, but the full source/readout tensor is missing", "next_action": "use the target only to test future parent-derived products"}),
        nonclaim({"row_id": "DEC2768_1_product_prediction", "decision": "do not score WEP alpha yet", "because": "beta_source_alpha, b_alpha/direct product, and tau_WEP remain unowned and the runner correctly refuses the product row", "next_action": "derive P_WEP_alpha directly from parent source-current geometry or prove a zero theorem"}),
        nonclaim({"row_id": "DEC2768_2_best_next", "decision": "next target is combined parent source-normalization and tau_WEP product theorem", "because": "separating beta_source_alpha from tau_WEP may be gauge/convention-dependent; the product is what the WEP bound actually tests", "next_action": "2769-Y5-R2FR-parent-source-normalization-tauWEP-product-theorem-or-WEP-alpha-closure-under-AX1090.md"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2768_0_2769",
            "next_target": "2769-Y5-R2FR-parent-source-normalization-tauWEP-product-theorem-or-WEP-alpha-closure-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_source_normalization_tauWEP_product_theorem_or_WEP_alpha_closure_under_AX1090_2769.py",
            "why": "2768 fills the WEP material target but not the MTS product. The next honest derivation attempt is the combined parent product theorem: prove P_WEP_alpha=0/direct numeric product from one source-current/local-geometry map, or demote WEP alpha to closure-only.",
            "include": "parent source-current owner, tau_WEP local geometry/readout map, direct P_WEP_alpha theorem route, zero-theorem clauses, surviving counterexamples, refusal row if any owner remains missing",
            "exclude": "beta_source_alpha=1, tau_WEP=1, cancellation, standalone b_alpha bound claim, public WEP/local-GR claim, GitHub action, formalization-workbench edits",
        })
    ]


def copy_branch_outputs(
    material: list[dict[str, Any]],
    derivation: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    prediction: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    failures: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    wep_rows = material + derivation + inputs + prediction + runner + failures + gates
    beta_rows = derivation + inputs + failures + next_rows
    microscope_rows = material + inputs + prediction + runner + gates + next_rows
    specs = [
        ("BR2768_0_wep_queue", "wep", wep_rows, OUTPUTS["prediction"], BRANCH_OUTPUTS["wep_queue"], "WEP alpha product input-fill nonclaim bundle"),
        ("BR2768_1_material_queue", "material", material, OUTPUTS["material"], BRANCH_OUTPUTS["material_queue"], "WEP material convention smoke-only copy"),
        ("BR2768_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["derivation"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing WEP input debt copy"),
        ("BR2768_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["material"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE WEP product input-fill copy"),
        ("BR2768_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next parent WEP product theorem target"),
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
    material = rows_by_name["material"]
    derivation = rows_by_name["derivation"]
    inputs = rows_by_name["inputs"]
    prediction = rows_by_name["prediction"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    comparisons = rows_by_name["comparisons"]
    failures = rows_by_name["failures"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2768_0_sources", all(row["exists"] and row["needles_found"] for row in sources), "every cited source path exists and needles are found"),
        ("VAL2768_1_material_convention_smoke_filled", any(row["row_id"] == "MCON2768_3_screened_product_target" and row["status"] == "score_threshold_filled_not_prediction" for row in material), "WEP material convention and product target are filled for smoke only"),
        ("VAL2768_2_beta_source_not_filled", any(row["row_id"] == "DER2768_1_beta_source_alpha" and "OWNER_NOT_DERIVED" in row["result"] for row in derivation), "beta_source_alpha remains owner-gated"),
        ("VAL2768_3_tau_WEP_not_filled", any(row["row_id"] == "DER2768_2_tau_WEP" and "DEFINITION_REQUIRED_NOT_FOUND" in row["result"] for row in derivation), "tau_WEP remains projection-gated"),
        ("VAL2768_4_input_ledger_blocks_unity", all(any(row["row_id"] == required_id and row["filled_status"] == "not_filled" for row in inputs) for required_id in ["INF2768_3_beta_source_alpha", "INF2768_4_tau_WEP", "INF2768_5_b_alpha_or_direct_product"]), "input ledger blocks beta/tau/product shortcuts"),
        ("VAL2768_5_prediction_template_nonclaim", prediction[0]["comparison_allowed"] is False and prediction[0]["claim_allowed"] is False and has_missing_marker(prediction[0]), "WEP prediction row remains nonclaim placeholder"),
        ("VAL2768_6_bound_import_numeric", bounds[0]["bound_value"] == "4.797780522732e-05" and is_numeric(bounds[0]["bound_value"]), "WEP product target is numeric"),
        ("VAL2768_7_product_runner_refuses", runner[0]["valid_prediction_rows"] == 0 and runner[0]["claim_allowed"] is False and comparisons[0]["comparison_status"] == "not_run", "product runner refuses missing parent product"),
        ("VAL2768_8_failure_modes_written", all(any(row["row_id"] == required_id for row in failures) for required_id in ["FAIL2768_0_no_beta_source_owner", "FAIL2768_1_no_tau_WEP_projection", "FAIL2768_3_no_unity_shortcuts"]), "strict failure modes are written"),
        ("VAL2768_9_claim_gates_blocked", all(row["gate_pass"] is False and row["claim_allowed"] is False for row in gates), "claim gates remain blocked"),
        ("VAL2768_10_next_target_written", any(row["row_id"] == "NEXT2768_0_2769" and "parent-source-normalization" in row["next_target"] for row in next_rows), "next target selects combined parent WEP product theorem"),
        ("VAL2768_11_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2768_12_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2768_13_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/allowed=true/pass_for_claim=true"),
        ("VAL2768_14_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2768_15_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2768_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2768_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2768 fills the WEP alpha material convention and screened product target for internal smoke testing, refuses beta_source_alpha/tau_WEP/b_alpha unity shortcuts, confirms no valid MTS P_WEP_alpha prediction exists, keeps all claim gates blocked, and selects the combined parent source-normalization tau_WEP product theorem or WEP-alpha closure as the next target.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2768 - Y5 R2/f(R): WEP Alpha Product First Input Fill tau_WEP / beta_source / Material Map Under AX1090",
        "## Private Verdict\n\nThe MICROSCOPE WEP material convention and screened alpha-product target are filled for internal smoke testing, but the MTS product prediction is still absent.\n\nNon-negotiable result: no WEP alpha pass is allowed until `P_WEP_alpha = beta_source_alpha*b_alpha*tau_WEP` is derived directly or every factor is parent-owned. No `beta_source_alpha=1`; no `tau_WEP=1`; no clock-only transfer.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "## WEP Material Convention\n\n" + markdown_table(rows_by_name["material"], ["row_id", "object", "definition", "numeric_value", "units", "source_row", "status", "blocks_claim", "valid_for_claim"]),
        "## beta_source / tau_WEP Derivation Attempt\n\n" + markdown_table(rows_by_name["derivation"], ["row_id", "target", "attempted_derivation", "available_evidence", "missing_premise", "result", "next_action", "valid_for_claim"]),
        "## Input Fill Ledger\n\n" + markdown_table(rows_by_name["inputs"], ["row_id", "required_input", "value_or_status", "source", "filled_status", "why_not_claim", "valid_for_claim"]),
        "## Alpha Product Prediction Attempt\n\n" + markdown_table(rows_by_name["prediction"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "inputs_present", "required_inputs", "derivation_status", "comparison_allowed", "claim_allowed", "valid_for_claim"]),
        "## Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_source", "source_row", "bound_type", "valid_for_claim", "notes"]),
        "## Product Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result", "valid_for_claim"]),
        "## Product Comparison Rows\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Strict Failure Modes\n\n" + markdown_table(rows_by_name["failures"], ["row_id", "object", "expected_failure", "observed_status", "meaning", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["row_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decision"], ["row_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "why", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis gives us the target board, not the dart. The lab-side WEP number is now in the current branch, but the theory still has to produce the coupling product from the parent action. That is the right next fight.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    inputs = load_inputs()
    sources = build_sources()
    material = build_material_rows(inputs)
    derivation = build_derivation_rows(inputs)
    input_rows = build_input_rows(inputs)
    prediction = build_prediction_rows()
    bounds = build_bound_rows(inputs)
    runner, comparisons = run_product_runner(prediction, bounds)
    failures = build_failures()
    gates = build_gates()
    decision = build_decision()
    next_rows = build_next()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["material"], material)
    write_csv(OUTPUTS["derivation"], derivation)
    write_csv(OUTPUTS["inputs"], input_rows)
    write_csv(OUTPUTS["prediction"], prediction)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["comparisons"], comparisons)
    write_csv(OUTPUTS["failures"], failures)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_rows)

    branches = copy_branch_outputs(material, derivation, input_rows, prediction, runner, failures, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "material": material,
        "derivation": derivation,
        "inputs": input_rows,
        "prediction": prediction,
        "bounds": bounds,
        "runner": runner,
        "comparisons": comparisons,
        "failures": failures,
        "gates": gates,
        "decision": decision,
        "next": next_rows,
        "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2768_OVERALL")
    print(f"2768 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
