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
DOC = WORK / "2771-Y5-R2FR-parent-category-label-forgetting-proof-or-relative-weight-runner-fill-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2771_SOURCE_REGISTER.csv",
    "proof": MTS / "P8_Y5_R2FR_2771_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
    "slot": MTS / "P8_Y5_R2FR_2771_NO_SOURCE_ONLY_SLOT_AUDIT.csv",
    "schema": MTS / "P8_Y5_R2FR_2771_RELATIVE_WEIGHT_RUNNER_SCHEMA.csv",
    "requirements": MTS / "P8_Y5_R2FR_2771_NUMERIC_SOURCE_REQUIREMENTS.csv",
    "guard": MTS / "P8_Y5_R2FR_2771_COMMON_MODE_GUARD.csv",
    "template": MTS / "P8_Y5_R2FR_2771_RELATIVE_WEIGHT_PRODUCT_TEMPLATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2771_RELATIVE_WEIGHT_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2771_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2771_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2771_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2771_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2771_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2771_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2771_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "proof_queue": RAB_QUEUE / "JR2771_PARENT_CATEGORY_LABEL_FORGETTING_NONCLAIM.csv",
    "runner_queue": RAB_QUEUE / "JR2771_RELATIVE_WEIGHT_RUNNER_FILL_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "PARENT_CATEGORY_LABEL_FORGETTING_2771_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "parent_category_label_forgetting_2771_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2771_NO_SOURCE_ONLY_SLOT_NEXT.csv",
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
        ("SRC2771_00_2770_next", "2770_next", MTS / "P8_Y5_R2FR_2770_NEXT_TARGET.csv", ["NEXT2770_0_2771"], "2770 handoff"),
        ("SRC2771_01_2770_proof", "2770_theorem", MTS / "P8_Y5_R2FR_2770_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv", ["THM2770_5_verdict"], "current R2/f(R) theorem verdict"),
        ("SRC2771_02_2770_owner", "2770_owner", MTS / "P8_Y5_R2FR_2770_NOETHER_SOURCE_OWNER_AUDIT.csv", ["NO2770_2_Noether_current_owner"], "current R2/f(R) owner audit"),
        ("SRC2771_03_2770_prior", "2770_prior", MTS / "P8_Y5_R2FR_2770_RELATIVE_WEIGHT_PRIOR_MATRIX.csv", ["RWP2770_4_delta_w_R10"], "current R2/f(R) relative-weight prior"),
        ("SRC2771_04_2770_template", "2770_template", MTS / "P8_Y5_R2FR_2770_RELATIVE_WEIGHT_PRODUCT_TEMPLATE_NONCLAIM.csv", ["PRED2770_0_WEP_relative_source_weight"], "current R2/f(R) product template"),
        ("SRC2771_05_1064_doc", "1064_doc", WORK / "1064-Y5-R10-parent-category-label-forgetting-proof-or-relative-weight-runner-fill.md", ["PLF1064_5_verdict"], "prior R10 label-forgetting proof/runner fill"),
        ("SRC2771_06_1064_proof", "1064_proof", MTS / "P8_Y5_R10_1064_LABEL_FORGETTING_PROOF_ATTEMPT.csv", ["PLF1064_5_verdict"], "prior proof attempt"),
        ("SRC2771_07_1064_slot", "1064_slot", MTS / "P8_Y5_R10_1064_NO_SOURCE_ONLY_SLOT_AUDIT.csv", ["NSS1064_2_relative_weight"], "prior no-source-only-slot audit"),
        ("SRC2771_08_1064_req", "1064_requirements", MTS / "P8_Y5_R10_1064_NUMERIC_SOURCE_REQUIREMENTS.csv", ["REQ1064_0_WEP_species"], "prior numeric requirements"),
        ("SRC2771_09_1064_guard", "1064_guard", MTS / "P8_Y5_R10_1064_COMMON_MODE_GUARD.csv", ["CMG1064_0_common_absorption"], "prior measured-G common-mode guard"),
        ("SRC2771_10_1064_template", "1064_template", MTS / "P8_Y5_R10_1064_RELATIVE_WEIGHT_PRODUCT_TEMPLATE_NONCLAIM.csv", ["PRED1064_0_WEP_relative_source_weight"], "prior product templates"),
        ("SRC2771_11_1064_bound", "1064_bound", MTS / "P8_Y5_R10_1064_RELATIVE_WEIGHT_BOUND_IMPORT.csv", ["BOUND1064_0_WEP_source_charge"], "prior bound import"),
        ("SRC2771_12_954_label_forgetting", "954_label_forgetting", MTS / "P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv", ["PLF954_5_verdict"], "parent label-forgetting attempt"),
        ("SRC2771_13_954_parent_clause", "954_parent_clause", MTS / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv", ["PAC954_1_no_source_prefactors"], "no source-prefactor clause"),
        ("SRC2771_14_954_bound_targets", "954_bound_targets", MTS / "P8_Y5_R10_954_SOURCE_FUNCTOR_BOUND_TARGETS.csv", ["SCB954_2_WEP_surface_beta_source"], "older species-weight bound targets"),
        ("SRC2771_15_954_countermodel", "954_countermodel", MTS / "P8_Y5_R10_954_COUNTERMODEL_TO_BOUND_MAP.csv", ["CBM954_0_labelled_weight"], "countermodel-to-bound map"),
        ("SRC2771_16_955_prefactor_class", "955_prefactor_class", MTS / "P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv", ["SPC955_2_relative_species_weight"], "source prefactor classes"),
        ("SRC2771_17_955_runner", "955_runner", MTS / "P8_Y5_R10_955_SPECIES_WEIGHT_RESIDUAL_RUNNER.csv", ["SWR955_3_WEP_coulomb_beta_source"], "older runner refusal rows"),
        ("SRC2771_18_956_spine", "956_spine", MTS / "P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv", ["SSG956_3_minimal_matter_action"], "source-side GR/Newton spine"),
        ("SRC2771_19_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", ["R9_Gdot"], "local empirical bound anchors"),
        ("SRC2771_20_393_doc", "393_doc", WORK / "393-source-normalized-Newtonian-limit-under-identity-closure.md", ["Only a constant, universal, range-independent"], "measured-G common-mode guard"),
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


def build_proof_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "PLF2771_0_target", "step": "parent category label-forgetting", "mathematical_form": "q_src({(T_A,A)}) = T_total before coupling selection; F_src(T_total)=kappa_univ T_total", "proof_result": "TARGET_RESTATED", "support": "THM2770_5_verdict; PLF1064_5_verdict", "gap": "target is not a derivation; parent category still must forbid labelled source arguments", "parent_signed": False}),
        nonclaim({"row_id": "PLF2771_1_total_Hilbert_variation", "step": "variation of a single matter action forgets bookkeeping labels after summation", "mathematical_form": "T_total = 2/sqrt(-g) delta(sum_A S_A)/delta g = sum_A T_A", "proof_result": "CONDITIONAL_MATH_CLEAN", "support": "PLF954_1_total_variation_route; MMA955_1_same_action_principle", "gap": "only works if the action being varied has no source-only prefactors w_A", "parent_signed": False}),
        nonclaim({"row_id": "PLF2771_2_no_source_only_slot", "step": "ban source-only species prefactors", "mathematical_form": "Allowed[S_matter] excludes w_A S_A when w_A has no nongravitational measurement role", "proof_result": "EXACT_CLAUSE_NOT_DERIVED", "support": "PAC954_1_no_source_prefactors; NSS1064_0_absent_slot", "gap": "absence of a slot is a parent action schema condition unless derived from deeper quotient/operator classification", "parent_signed": False}),
        nonclaim({"row_id": "PLF2771_3_counterexample", "step": "relative-weight obstruction", "mathematical_form": "S_matter=sum_A w_A S_A gives T_source=sum_A w_A T_A while preserving covariance/additivity", "proof_result": "COUNTEREXAMPLE_SURVIVES", "support": "CE2769_1_relative_source_weight; SPC955_2_relative_species_weight", "gap": "field rescalings do not generally remove w_A once interactions, charges, and quantum normalization are measured", "parent_signed": False}),
        nonclaim({"row_id": "PLF2771_4_no_hidden_spurion_return", "step": "prevent disguised source labels", "mathematical_form": "partial_m kappa = partial_D kappa = partial_boundary kappa = partial_readout kappa = 0", "proof_result": "PARALLEL_GATE_UNSIGNED", "support": "PAC954_3_no_hidden_spurion_return; SPC955_3_hidden_marker_weight", "gap": "no-marker/no-extension theorem remains rejected or conditional in current corpus", "parent_signed": False}),
        nonclaim({"row_id": "PLF2771_5_verdict", "step": "parent category label-forgetting proof", "mathematical_form": "single S_matter + no w_A + no hidden spurion return + total Hilbert variation => source labels forgotten", "proof_result": "CONDITIONAL_CONTRACT_NOT_PARENT_DERIVED", "support": "953/954/955/956/1063/2770 chain", "gap": "no-source-only-slot theorem is not signed; relative-weight runner fill is required", "parent_signed": False}),
    ]


def build_slot_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "NSS2771_0_absent_slot", "slot": "w_A source-only prefactor", "allowed_status": "desired_absent_slot", "required_signature": "parent action grammar has no argument corresponding to source-only species weight", "if_present": "relative source WEP/PPN/R10 residual", "current_status": "not_parent_signed"}),
        nonclaim({"row_id": "NSS2771_1_common_mode", "slot": "w_common", "allowed_status": "calibration_only", "required_signature": "constant universal range/time/species/frame independent multiplier", "if_present": "absorbed into measured G only after all derivative/common-mode guards pass", "current_status": "guarded_not_claim"}),
        nonclaim({"row_id": "NSS2771_2_relative_weight", "slot": "epsilon_A with w_A=w_common(1+epsilon_A)", "allowed_status": "live_countermodel_if_not_forbidden", "required_signature": "numeric epsilon_A vector with source path or parent theorem-zero", "if_present": "WEP/source charge and possibly PPN/R10 residuals", "current_status": "retained_nonclaim"}),
        nonclaim({"row_id": "NSS2771_3_nonHilbert_weight", "slot": "zeta_A J_NH,A", "allowed_status": "parallel_open_gate", "required_signature": "non-Hilbert current is absent, exact/projected silent, or explicitly bounded", "if_present": "bypasses Hilbert-current source theorem", "current_status": "retained_separate_gate"}),
    ]


def build_schema_rows() -> list[dict[str, Any]]:
    columns = [
        "prediction_id", "arena", "product_symbol", "product_value", "product_units", "product_source",
        "inputs_present", "required_inputs", "derivation_status", "valid_for_claim", "notes",
    ]
    return [nonclaim({"column": column, "definition": {
        "prediction_id": "stable row id",
        "arena": "MICROSCOPE_WEP, PPN_Newton, Gdot_orbital, or R10_short_range",
        "product_symbol": "exact relative-weight product tested",
        "product_value": "numeric prediction only; placeholders are invalid",
        "product_units": "dimensionless, yr^-1, or declared alpha(lambda) convention",
        "product_source": "local source path proving the product",
        "inputs_present": "semicolon-separated real inputs",
        "required_inputs": "all required coefficients/maps/source files",
        "derivation_status": "derived_zero, sourced_numeric, or blocked status",
        "valid_for_claim": "true only when numeric/sourced/unit matched",
        "notes": "assumptions and no-cancellation caveats",
    }[column], "required": True, "nonclaim_rule": "reject if missing marker, nonnumeric product, unity shortcut, source missing, or valid_for_claim=false"}) for column in columns]


def build_requirement_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "REQ2771_0_WEP_species", "arena": "MICROSCOPE_WEP", "product_symbol": "P_WEP_relative_source_weight", "required_inputs": "species_pair;Delta_w_AB;tau_WEP;material/source map;eta_prediction;source_file", "units": "dimensionless", "bound_or_target": "2.8e-15", "source_requirement": "parent label-forgetting theorem or sourced Delta_w_AB and tau_WEP map", "current_status": "MISSING_DELTA_W_AB_TAU_WEP_PRODUCT"}),
        nonclaim({"row_id": "REQ2771_1_PPN_gamma", "arena": "PPN_Newton", "product_symbol": "P_PPN_source_weight_gamma", "required_inputs": "C_gamma_source_weight;Delta_w_source;weak_field_response_map;source_file", "units": "dimensionless", "bound_or_target": "2.3e-05", "source_requirement": "weak-field PPN response from relative weights into gamma-1 or theorem-zero", "current_status": "MISSING_C_GAMMA_SOURCE_WEIGHT_PRODUCT"}),
        nonclaim({"row_id": "REQ2771_2_PPN_beta", "arena": "PPN_Newton", "product_symbol": "P_PPN_source_weight_beta", "required_inputs": "C_beta_source_weight;Delta_w_source;second_order_response_map;source_file", "units": "dimensionless", "bound_or_target": "7.8e-05", "source_requirement": "second-order PPN source response or theorem-zero", "current_status": "MISSING_C_BETA_SOURCE_WEIGHT_PRODUCT"}),
        nonclaim({"row_id": "REQ2771_3_Gdot", "arena": "Gdot_orbital", "product_symbol": "P_Gdot_relative_source_weight", "required_inputs": "dln_w_source_dt;time_map;source-frame convention;source_file", "units": "yr^-1", "bound_or_target": "9.6e-15", "source_requirement": "time constancy theorem or sourced drift below LLR lock", "current_status": "MISSING_DLN_W_SOURCE_DT"}),
        nonclaim({"row_id": "REQ2771_4_R10", "arena": "R10_short_range", "product_symbol": "P_R10_relative_weight(lambda)", "required_inputs": "lambda_w;K_w(lambda);Delta_w_source;Delta_w_test;tau_R10;alpha_bound(lambda);source_file", "units": "dimensionless with length column", "bound_or_target": "promoted alpha(lambda) curve", "source_requirement": "finite-range product and bound curve, or no finite-range source-weight theorem", "current_status": "MISSING_KW_DELTAW_SOURCE_DELTAW_TEST_TAU_R10_PRODUCT"}),
    ]


def build_guard_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CMG2771_0_common_absorption", "candidate_absorption": "w_common into measured G", "required_zero_derivatives": "D_A=0;D_t=0;D_r=0;D_lambda=0;Delta_frame=0", "must_be": "constant;universal;range_independent;time_independent;species_blind;same_frame", "current_status": "not_proved", "if_failed": "relative/source-normalization residual remains physical"}),
        nonclaim({"row_id": "CMG2771_1_relative_not_absorbable", "candidate_absorption": "epsilon_A relative source weights into G", "required_zero_derivatives": "Delta_AB epsilon=0 for every source/test material pair", "must_be": "species_blind before calibration", "current_status": "not_proved", "if_failed": "WEP/source charge residual cannot be hidden in G"}),
        nonclaim({"row_id": "CMG2771_2_range_not_absorbable", "candidate_absorption": "finite-range source weight into local calibration", "required_zero_derivatives": "D_lambda=0 and D_r=0 across tested range", "must_be": "range_independent before R10/orbital comparison", "current_status": "not_proved", "if_failed": "R10/orbital/fifth-force row must be filled"}),
    ]


def build_prediction_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"prediction_id": "PRED2771_0_WEP_relative_source_weight", "arena": "MICROSCOPE_WEP", "product_symbol": "P_WEP_relative_source_weight", "product_value": "MISSING_DELTA_W_AB_TAU_WEP_PRODUCT", "product_units": "dimensionless", "required_inputs": "species_pair;Delta_w_AB;tau_WEP;material/source map;eta_prediction;source_file", "derivation_status": "MISSING_NUMERIC_OR_THEOREM_ZERO_RELATIVE_WEIGHT"}),
        nonclaim({"prediction_id": "PRED2771_1_PPN_gamma_source_weight", "arena": "PPN_Newton", "product_symbol": "P_PPN_source_weight_gamma", "product_value": "MISSING_C_GAMMA_SOURCE_WEIGHT_PRODUCT", "product_units": "dimensionless", "required_inputs": "C_gamma_source_weight;Delta_w_source;weak_field_response_map;source_file", "derivation_status": "MISSING_RESPONSE_OPERATOR"}),
        nonclaim({"prediction_id": "PRED2771_2_PPN_beta_source_weight", "arena": "PPN_Newton", "product_symbol": "P_PPN_source_weight_beta", "product_value": "MISSING_C_BETA_SOURCE_WEIGHT_PRODUCT", "product_units": "dimensionless", "required_inputs": "C_beta_source_weight;Delta_w_source;second_order_response_map;source_file", "derivation_status": "MISSING_RESPONSE_OPERATOR"}),
        nonclaim({"prediction_id": "PRED2771_3_Gdot_relative_source_weight", "arena": "Gdot_orbital", "product_symbol": "P_Gdot_relative_source_weight", "product_value": "MISSING_DLN_W_SOURCE_DT", "product_units": "yr^-1", "required_inputs": "dln_w_source_dt;time_map;source-frame convention;source_file", "derivation_status": "MISSING_TIME_MAP"}),
        nonclaim({"prediction_id": "PRED2771_4_R10_relative_weight_lambda", "arena": "R10_short_range", "product_symbol": "P_R10_relative_weight(lambda)", "product_value": "MISSING_KW_DELTAW_SOURCE_DELTAW_TEST_TAU_R10_PRODUCT", "product_units": "dimensionless", "required_inputs": "lambda_w;K_w(lambda);Delta_w_source;Delta_w_test;tau_R10;alpha_bound(lambda);source_file", "derivation_status": "MISSING_R10_RELATIVE_WEIGHT_PRODUCT"}),
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"bound_id": "BOUND2771_0_WEP_source_charge", "arena": "MICROSCOPE_WEP", "product_symbol": "P_WEP_relative_source_weight", "bound_value": "2.8e-15", "bound_units": "dimensionless", "bound_type": "numeric_bound_nonclaim"}),
        nonclaim({"bound_id": "BOUND2771_1_PPN_gamma", "arena": "PPN_Newton", "product_symbol": "P_PPN_source_weight_gamma", "bound_value": "2.3e-05", "bound_units": "dimensionless", "bound_type": "numeric_bound_nonclaim"}),
        nonclaim({"bound_id": "BOUND2771_2_PPN_beta", "arena": "PPN_Newton", "product_symbol": "P_PPN_source_weight_beta", "bound_value": "7.8e-05", "bound_units": "dimensionless", "bound_type": "numeric_bound_nonclaim"}),
        nonclaim({"bound_id": "BOUND2771_3_Gdot", "arena": "Gdot_orbital", "product_symbol": "P_Gdot_relative_source_weight", "bound_value": "9.6e-15", "bound_units": "yr^-1", "bound_type": "numeric_bound_nonclaim"}),
        nonclaim({"bound_id": "BOUND2771_4_R10_alpha_lambda", "arena": "R10_short_range", "product_symbol": "P_R10_relative_weight(lambda)", "bound_value": "MISSING_PROMOTED_ALPHA_LAMBDA_CURVE", "bound_units": "range-dependent", "bound_type": "symbolic_curve_required"}),
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
    valid_predictions = [row for row in predictions if row.get("valid_for_claim") is True and is_numeric(row.get("product_value")) and not has_missing_marker(row)]
    valid_bounds = [row for row in bounds if is_numeric(row.get("bound_value")) and float(str(row["bound_value"])) > 0.0 and not has_missing_marker(row)]
    comparisons = [nonclaim({"comparison_id": "PRODUCT_COMPARE_NO_VALID_PREDICTIONS", "arena": "", "product_symbol": "", "product_value": "", "bound_value": "", "comparison_status": "not_run", "pass_for_claim": False, "issues": "no valid MTS relative-weight product prediction rows"})]
    runner = [nonclaim({"runner_id": "APR2771_0_relative_weight_strict_product_runner", "prediction_rows": len(predictions), "bound_rows": len(bounds), "valid_prediction_rows": len(valid_predictions), "valid_bound_rows": len(valid_bounds), "comparison_rows": len(comparisons), "claim_allowed": False, "expected_result": "reject_all_missing_relative_weight_products"})]
    return runner, comparisons


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CG2771_0_label_forgetting_proof", "claim": "parent category label-forgetting is proved", "gate_pass": False, "reason": "no-source-only-slot theorem remains an exact clause, not a parent derivation", "claim_allowed": False}),
        nonclaim({"row_id": "CG2771_1_no_wA_slot", "claim": "w_A source-only prefactor is forbidden", "gate_pass": False, "reason": "relative prefactor counterexample survives unless parent action grammar forbids it", "claim_allowed": False}),
        nonclaim({"row_id": "CG2771_2_relative_weight_runner_scores", "claim": "relative-weight WEP/PPN/Gdot/R10 products score", "gate_pass": False, "reason": "strict runner has valid_prediction_rows=0 and R10 bound curve remains unpromoted", "claim_allowed": False}),
        nonclaim({"row_id": "CG2771_3_measured_G_absorption", "claim": "relative weights can be absorbed into measured G", "gate_pass": False, "reason": "only common universal range/time/species/frame independent normalization is absorbable", "claim_allowed": False}),
        nonclaim({"row_id": "CG2771_4_local_GR_Newton", "claim": "local GR/Newton source side is derived", "gate_pass": False, "reason": "source-side coupling remains conditional and EH/R11/PPN readout gates remain open", "claim_allowed": False}),
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "DEC2771_0_proof_status", "decision": "parent category label-forgetting proof remains conditional", "because": "the no-source-only-slot clause is exact but not derived from deeper MTS primitives", "next_action": "keep as parent-action contract and do not promote universal coupling"}),
        nonclaim({"row_id": "DEC2771_1_runner_status", "decision": "strict relative-weight runner contract is filled", "because": "WEP, PPN gamma/beta, Gdot, and R10 now have exact numeric/source requirements and refusal rows", "next_action": "fill one product row numerically or derive the no-w_A theorem"}),
        nonclaim({"row_id": "DEC2771_2_best_next", "decision": "next target is the no-source-only-slot parent grammar", "because": "this is the smallest theorem that would remove w_A rather than bounding it", "next_action": "2772-Y5-R2FR-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row-under-AX1090.md"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2771_0_2772",
            "next_target": "2772-Y5-R2FR-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_no_source_only_slot_parent_grammar_or_first_relative_weight_numeric_row_under_AX1090_2772.py",
            "why": "the exact remaining theorem is whether parent action grammar can exclude source-only species scalar w_A; if not, the first WEP relative-weight row needs numeric/source requirements",
            "include": "allowed-action grammar, field normalization loopholes, interaction/charge normalization, w_A theorem-zero clauses, first WEP numeric row schema if theorem fails",
            "exclude": "assuming minimality, absorbing relative weights into measured G, unity shortcuts, cancellation, public local-GR/WEP/R10 claim, GitHub action, formalization-workbench edits",
        })
    ]


def copy_branch_outputs(
    proof: list[dict[str, Any]],
    slot: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    template: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    proof_rows = proof + slot
    runner_rows = requirements + template + gates
    beta_rows = slot + requirements + next_rows
    microscope_rows = [row for row in requirements + template if "WEP" in str(row.get("arena", row.get("product_symbol", "")))] + gates + next_rows
    specs = [
        ("BR2771_0_proof_queue", "proof", proof_rows, OUTPUTS["proof"], BRANCH_OUTPUTS["proof_queue"], "parent-category label-forgetting proof"),
        ("BR2771_1_runner_queue", "runner", runner_rows, OUTPUTS["requirements"], BRANCH_OUTPUTS["runner_queue"], "relative-weight runner fill"),
        ("BR2771_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["slot"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing label-forgetting copy"),
        ("BR2771_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["template"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE relative-weight runner copy"),
        ("BR2771_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next no-source-only-slot target"),
    ]
    rows = []
    for copy_id, table_key, source_rows, source_table, copy_path, purpose in specs:
        write_csv(copy_path, source_rows)
        rows.append(nonclaim({"copy_id": copy_id, "table_key": table_key, "source_table": rel(source_table), "copy_path": rel(copy_path), "purpose": purpose, "exists": copy_path.exists(), "row_count": csv_row_count(copy_path) if copy_path.exists() else 0}))
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
            if str(row.get("pass_for_claim", "False")).lower() == "true":
                return False
    return True


def remove_pycache() -> None:
    pycache = SCRIPTS / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    proof = rows_by_name["proof"]
    slot = rows_by_name["slot"]
    schema = rows_by_name["schema"]
    requirements = rows_by_name["requirements"]
    guard = rows_by_name["guard"]
    template = rows_by_name["template"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2771_0_sources", all(row["exists"] and row["needles_found"] for row in sources), "every cited source path exists and needles are found"),
        ("VAL2771_1_label_forgetting_not_promoted", any(row["row_id"] == "PLF2771_5_verdict" and row["proof_result"] == "CONDITIONAL_CONTRACT_NOT_PARENT_DERIVED" for row in proof), "label-forgetting proof remains conditional"),
        ("VAL2771_2_wA_slot_retained", any(row["row_id"] == "NSS2771_2_relative_weight" and row["current_status"] == "retained_nonclaim" for row in slot), "relative source-weight slot is retained as nonclaim countermodel"),
        ("VAL2771_3_runner_schema_written", len(schema) >= 11 and all(row["required"] is True for row in schema), "strict product-runner schema written"),
        ("VAL2771_4_numeric_requirements_written", all(any(row["row_id"] == required for row in requirements) for required in ["REQ2771_0_WEP_species", "REQ2771_1_PPN_gamma", "REQ2771_3_Gdot", "REQ2771_4_R10"]), "WEP, PPN, Gdot, and R10 numeric/source requirements written"),
        ("VAL2771_5_common_mode_guard_written", len(guard) >= 3 and any(row["row_id"] == "CMG2771_0_common_absorption" for row in guard), "measured-G common-mode guard written"),
        ("VAL2771_6_prediction_templates_nonclaim", all(row["valid_for_claim"] is False and has_missing_marker(row) for row in template), "all relative-weight prediction templates remain missing-input placeholders"),
        ("VAL2771_7_bound_import_written", all(any(row["bound_id"] == required for row in bounds) for required in ["BOUND2771_0_WEP_source_charge", "BOUND2771_1_PPN_gamma", "BOUND2771_3_Gdot"]), "WEP/PPN/Gdot bound anchors imported and R10 remains curve-required"),
        ("VAL2771_8_product_runner_refuses_placeholders", runner[0]["valid_prediction_rows"] == 0 and runner[0]["claim_allowed"] is False, "product runner refuses all strict relative-weight placeholders"),
        ("VAL2771_9_claim_gates_blocked", all(row["gate_pass"] is False and row["claim_allowed"] is False for row in gates), "all label-forgetting and relative-weight claim gates remain blocked"),
        ("VAL2771_10_next_target_written", any(row["row_id"] == "NEXT2771_0_2772" and "no-source-only-slot" in row["next_target"] for row in next_rows), "next target selects no-source-only-slot grammar or first numeric row"),
        ("VAL2771_11_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2771_12_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2771_13_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2771_14_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2771_15_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2771_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({"validation_id": "VAL2771_OVERALL", "passed": all(row["passed"] for row in rows), "detail": "2771 states the parent-category label-forgetting proof in the current R2/f(R) branch, keeps no-source-only-slot conditional, fills strict WEP/PPN/Gdot/R10 relative-weight runner requirements, blocks measured-G absorption of relative weights, refuses all placeholders, and selects no-source-only-slot parent grammar or first WEP numeric row as the next target.", "timestamp_utc": ts()})
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2771 - Y5 R2/f(R): Parent Category Label-Forgetting Proof Or Relative-Weight Runner Fill Under AX1090",
        "## Private Verdict\n\nLabel-forgetting is still a conditional parent-action contract, not a theorem. The exact missing clause is the no-source-only-slot rule for `w_A`.\n\nRunner result: the strict relative-weight runner contract now covers WEP, PPN gamma, PPN beta, Gdot, and R10, and it refuses all current placeholders.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "## Parent Label-Forgetting Proof Attempt\n\n" + markdown_table(rows_by_name["proof"], ["row_id", "step", "mathematical_form", "proof_result", "support", "gap", "parent_signed", "valid_for_claim"]),
        "## No-Source-Only-Slot Audit\n\n" + markdown_table(rows_by_name["slot"], ["row_id", "slot", "allowed_status", "required_signature", "if_present", "current_status", "valid_for_claim"]),
        "## Strict Runner Schema\n\n" + markdown_table(rows_by_name["schema"], ["column", "definition", "required", "nonclaim_rule", "valid_for_claim"]),
        "## Numeric Source Requirements\n\n" + markdown_table(rows_by_name["requirements"], ["row_id", "arena", "product_symbol", "required_inputs", "units", "bound_or_target", "source_requirement", "current_status", "valid_for_claim"]),
        "## Measured-G Common-Mode Guard\n\n" + markdown_table(rows_by_name["guard"], ["row_id", "candidate_absorption", "required_zero_derivatives", "must_be", "current_status", "if_failed", "valid_for_claim"]),
        "## Product Prediction Templates\n\n" + markdown_table(rows_by_name["template"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "required_inputs", "derivation_status", "valid_for_claim"]),
        "## Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "valid_for_claim"]),
        "## Product Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result", "valid_for_claim"]),
        "## Product Comparison Rows\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["row_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decision"], ["row_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "why", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis narrows the universal-coupling problem to one wickedly precise question: does the parent language even allow a source-only species scalar? If the answer is no, `w_A` dies as a theorem. If the answer is yes or unsigned, we start filling the WEP relative-weight row honestly.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    proof = build_proof_rows()
    slot = build_slot_rows()
    schema = build_schema_rows()
    requirements = build_requirement_rows()
    guard = build_guard_rows()
    template = build_prediction_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(template, bounds)
    gates = build_gates()
    decision = build_decision()
    next_rows = build_next()

    for key, rows in [
        ("sources", sources), ("proof", proof), ("slot", slot), ("schema", schema), ("requirements", requirements),
        ("guard", guard), ("template", template), ("bounds", bounds), ("runner", runner), ("comparisons", comparisons),
        ("gates", gates), ("decision", decision), ("next", next_rows),
    ]:
        write_csv(OUTPUTS[key], rows)

    branches = copy_branch_outputs(proof, slot, requirements, template, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources, "proof": proof, "slot": slot, "schema": schema, "requirements": requirements,
        "guard": guard, "template": template, "bounds": bounds, "runner": runner, "comparisons": comparisons,
        "gates": gates, "decision": decision, "next": next_rows, "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2771_OVERALL")
    print(f"2771 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
