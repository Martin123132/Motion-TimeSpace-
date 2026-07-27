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
DOC = WORK / "2770-Y5-R2FR-source-label-forgetting-Noether-current-owner-or-relative-weight-prior-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2770_SOURCE_REGISTER.csv",
    "theorem": MTS / "P8_Y5_R2FR_2770_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv",
    "owner": MTS / "P8_Y5_R2FR_2770_NOETHER_SOURCE_OWNER_AUDIT.csv",
    "prior": MTS / "P8_Y5_R2FR_2770_RELATIVE_WEIGHT_PRIOR_MATRIX.csv",
    "template": MTS / "P8_Y5_R2FR_2770_RELATIVE_WEIGHT_PRODUCT_TEMPLATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2770_RELATIVE_WEIGHT_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2770_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2770_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2770_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2770_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2770_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2770_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2770_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_queue": RAB_QUEUE / "JR2770_SOURCE_LABEL_FORGETTING_THEOREM_NONCLAIM.csv",
    "prior_queue": RAB_QUEUE / "JR2770_RELATIVE_WEIGHT_PRIOR_MATRIX_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "SOURCE_LABEL_NOETHER_RELATIVE_WEIGHT_2770_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "source_label_noether_relative_weight_2770_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2770_PARENT_CATEGORY_LABEL_FORGETTING_NEXT.csv",
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
        ("SRC2770_00_2769_next", "2769_next", MTS / "P8_Y5_R2FR_2769_NEXT_TARGET.csv", ["NEXT2769_0_2770"], "2769 handoff"),
        ("SRC2770_01_2769_premise", "2769_premise", MTS / "P8_Y5_R2FR_2769_PREMISE_SIGNATURE_AUDIT.csv", ["PREM2769_3_source_label_forgetting"], "current source-label premise"),
        ("SRC2770_02_2769_counterexample", "2769_counterexample", MTS / "P8_Y5_R2FR_2769_COUNTEREXAMPLE_SURVIVAL_LEDGER.csv", ["CE2769_1_relative_source_weight"], "current relative-weight counterexample"),
        ("SRC2770_03_1063_doc", "1063_doc", WORK / "1063-Y5-R10-source-label-forgetting-Noether-current-owner-or-relative-weight-prior.md", ["THM1063_5_verdict"], "prior R10 source-label/Noether audit"),
        ("SRC2770_04_1063_theorem", "1063_theorem", MTS / "P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv", ["THM1063_5_verdict"], "prior theorem attempt"),
        ("SRC2770_05_1063_owner", "1063_owner", MTS / "P8_Y5_R10_1063_NOETHER_SOURCE_OWNER_AUDIT.csv", ["NO1063_2_Noether_current_owner"], "prior Noether owner audit"),
        ("SRC2770_06_1063_prior", "1063_prior", MTS / "P8_Y5_R10_1063_RELATIVE_WEIGHT_PRIOR_MATRIX.csv", ["RWP1063_4_delta_w_R10"], "prior relative-weight matrix"),
        ("SRC2770_07_953_source_functor", "953_source_functor", MTS / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv", ["NSF953_5_verdict"], "source-functor theorem attempt"),
        ("SRC2770_08_955_matter_lemma", "955_matter_lemma", MTS / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv", ["MMA955_6_verdict"], "minimal matter action lemma"),
        ("SRC2770_09_989_parent_input", "989_parent_input", MTS / "P8_Y5_R10_989_PARENT_INPUT_CANDIDATE_LEDGER.csv", ["PIC989_2_Noether_current_owner"], "Noether/current/source owner input"),
        ("SRC2770_10_989_EM_lock", "989_EM_lock", MTS / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", ["ELA989_2_current_owner"], "EM current owner audit"),
        ("SRC2770_11_1055_counterexample", "1055_counterexample", MTS / "P8_Y5_R10_1055_COUNTEREXAMPLE_LEDGER.csv", ["CE1055_3_relative_source_weight"], "relative source-weight ledger"),
        ("SRC2770_12_1044_pullback", "1044_pullback", MTS / "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv", ["MPD1044_6_source_current_universality"], "matter source-current universality gap"),
        ("SRC2770_13_990_contract", "990_contract", MTS / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv", ["PAC990_4_source_charge"], "minimal parent source charge contract"),
        ("SRC2770_14_393_doc", "393_doc", WORK / "393-source-normalized-Newtonian-limit-under-identity-closure.md", ["Only a constant, universal, range-independent"], "measured-G common-mode rule"),
        ("SRC2770_15_639_matrix", "639_matrix", MTS / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv", ["LBM639_10"], "local WEP/PPN/R10 bound matrix"),
        ("SRC2770_16_708_map", "708_map", MTS / "P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv", ["PGW708_4_R10_alpha"], "PPN/Gdot/WEP/R10 projection map"),
        ("SRC2770_17_768_GR_Newton", "768_GR_Newton", MTS / "P8_Y5_R10_768_GR_NEWTON_REQUIREMENT_MAP.csv", ["GN768_2_source_charge"], "GR/Newton source charge requirement"),
        ("SRC2770_18_768_live_edge", "768_live_edge", MTS / "P8_Y5_R10_768_R11_SOURCE_NORMALIZATION_LIVE_EDGE.csv", ["RSN768_0_cmu_sum_rule"], "source-normalization live edge"),
        ("SRC2770_19_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", ["R1_WEP_source_charge"], "local WEP/PPN/Gdot bound anchors"),
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


def build_theorem_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "THM2770_0_target", "claim_shape": "derive species-blind source-label forgetting and one Noether/Hilbert current owner", "formal_statement": "Admissible source functor should take T_total as input, not labelled pairs (T_A,A).", "attempt_result": "TARGET_RESTATED", "why_it_matters": "if labels are absent, relative source weights kappa_A/kappa_B cannot be formed", "current_gap": "parent matter category still exposes labels unless a deeper quotient forgets them"}),
        nonclaim({"row_id": "THM2770_1_additivity", "claim_shape": "covariance plus additivity gives a unique source current", "formal_statement": "F_src(T_A+T_B)=F_src(T_A)+F_src(T_B) removes nonlinear source mixing.", "attempt_result": "INSUFFICIENT_ALONE", "why_it_matters": "it is a useful theorem ingredient, but not enough", "current_gap": "F((T_A,A))=kappa_A T_A is still additive and covariant"}),
        nonclaim({"row_id": "THM2770_2_same_action_Hilbert_source", "claim_shape": "same S_matter gives equations of motion and Hilbert stress source", "formal_statement": "E_A=delta S_matter/delta Psi_A and T_A=2/sqrt(-g) delta S_A/delta g_obs.", "attempt_result": "STRONG_CONDITIONAL_LEMMA", "why_it_matters": "rules out a separate arbitrary source functional", "current_gap": "constant relative prefactors w_A inside S_A survive unless parent minimality is signed"}),
        nonclaim({"row_id": "THM2770_3_Noether_current_owner", "claim_shape": "same parent Noether owner fixes charge labels, matter coupling, and source normalization", "formal_statement": "one parent current J_owner produces observed source/test coupling with no species-only coefficient slot", "attempt_result": "OWNER_NOT_DERIVED", "why_it_matters": "would close beta_source_alpha-like source normalization debts", "current_gap": "PIC989_2 and ELA989_2 still mark Noether/current owner as candidate-missing/unsigned"}),
        nonclaim({"row_id": "THM2770_4_measured_G_absorption", "claim_shape": "measured G can absorb source normalization", "formal_statement": "only common, universal, range-independent source normalization may be absorbed into measured G", "attempt_result": "COMMON_MODE_ONLY", "why_it_matters": "prevents fake Newton wins", "current_gap": "relative, range-dependent, radial, time-dependent, or species-labelled weights remain physical residuals"}),
        nonclaim({"row_id": "THM2770_5_verdict", "claim_shape": "source-label forgetting / Noether current theorem", "formal_statement": "label-forgotten source functor + same-action Hilbert source + current owner => one universal source normalization", "attempt_result": "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED", "why_it_matters": "this is the clean path to GR-style universal coupling", "current_gap": "relative w_A counterexample survives current corpus"}),
    ]


def build_owner_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "NO2770_0_source_functor_domain", "object": "source functor domain", "required_owner": "parent category maps ordinary matter to T_total before source coupling selection", "current_status": "label_forgetting_not_parent_signed", "if_missing": "kappa_A T_A survives as a legal additive source", "source": "NSF953_1_domain_fork; NSF953_5_verdict"}),
        nonclaim({"row_id": "NO2770_1_same_action_Hilbert_current", "object": "Hilbert matter source", "required_owner": "same S_matter supplies matter equations and gravitational source", "current_status": "conditional_lemma_not_parent_derivation", "if_missing": "separate source current or relative prefactor can be inserted", "source": "MMA955_1_same_action_principle; MMA955_6_verdict"}),
        nonclaim({"row_id": "NO2770_2_Noether_current_owner", "object": "Noether/current/source normalization", "required_owner": "single parent Noether owner fixes charge unit, matter coupling, and source/test normalization", "current_status": "candidate_missing", "if_missing": "beta_source_alpha and relative source weights remain free finite-branch debts", "source": "PIC989_2_Noether_current_owner; ELA989_2_current_owner"}),
        nonclaim({"row_id": "NO2770_3_Hamiltonian_source_charge", "object": "measured Newtonian source mass", "required_owner": "integrable fixed-reference Hamiltonian source charge with same-frame source measure", "current_status": "selected_live_edge_not_closed", "if_missing": "EH-looking equations still lack measured Newtonian GM/source normalization", "source": "PAC990_4_source_charge; GN768_2_source_charge"}),
    ]


def build_prior_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "RWP2770_0_common_weight", "quantity": "w_common", "definition": "one common multiplier on the whole matter/source action", "observable_channel": "measured_G_common_mode", "current_status": "absorbable_only_if_constant_universal_range_independent", "required_for_claim": "prove no species, time, radial, range, or frame dependence before absorption", "bound_or_target": "calibration_only_not_a_test_pass"}),
        nonclaim({"row_id": "RWP2770_1_delta_w_WEP", "quantity": "Delta_w_AB", "definition": "relative source weight contrast between MICROSCOPE test materials", "observable_channel": "WEP_source_charge_eta_AB", "current_status": "MISSING_NUMERIC_OR_THEOREM_ZERO_RELATIVE_WEIGHT", "required_for_claim": "parent label-forgetting theorem or sourced Delta_w_AB with tau_WEP/material map", "bound_or_target": "eta_AB <= 2.8e-15"}),
        nonclaim({"row_id": "RWP2770_2_delta_w_PPN", "quantity": "C_PPN_source_weight * Delta_w_source", "definition": "source normalization response of PPN gamma/beta to relative source weights", "observable_channel": "PPN_gamma_beta_Newton_source_normalization", "current_status": "MISSING_RESPONSE_OPERATOR", "required_for_claim": "weak-field response map from relative source weights into gamma/beta or theorem-zero", "bound_or_target": "gamma-1 <= 2.3e-05; beta-1 <= 7.8e-05"}),
        nonclaim({"row_id": "RWP2770_3_delta_w_Gdot", "quantity": "d_t ln w_source", "definition": "time drift of source normalization if relative source weights move", "observable_channel": "Gdot_over_G", "current_status": "MISSING_TIME_MAP", "required_for_claim": "time map and proof that any surviving source weight is constant or below bound", "bound_or_target": "Gdot/G <= 9.6e-15 yr^-1"}),
        nonclaim({"row_id": "RWP2770_4_delta_w_R10", "quantity": "K_w(lambda) Delta_w_source Delta_w_test", "definition": "finite-range relative-weight source/test product for inverse-square/R10 tests", "observable_channel": "R10_alpha_lambda", "current_status": "MISSING_KW_LAMBDA_SOURCE_TEST_WEIGHTS", "required_for_claim": "range, coupling normalization, source/test weights, tau_R10, and promoted alpha(lambda) bound curve", "bound_or_target": "alpha(lambda) curve required"}),
    ]


def build_prediction_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"prediction_id": "PRED2770_0_WEP_relative_source_weight", "arena": "MICROSCOPE_WEP", "product_symbol": "P_WEP_relative_source_weight", "product_value": "MISSING_DELTA_W_AB_TAU_WEP_PRODUCT", "product_units": "dimensionless", "required_inputs": "Delta_w_TA6V_minus_PtRh10;tau_WEP;source-label-forgetting theorem OR numeric product", "derivation_status": "MISSING_NUMERIC_OR_THEOREM_ZERO_RELATIVE_WEIGHT"}),
        nonclaim({"prediction_id": "PRED2770_1_PPN_gamma_source_weight", "arena": "PPN_Newton", "product_symbol": "P_PPN_source_weight_gamma", "product_value": "MISSING_C_GAMMA_SOURCE_WEIGHT_PRODUCT", "product_units": "dimensionless", "required_inputs": "C_gamma_source_weight;Delta_w_source;weak_field_response_map OR theorem-zero", "derivation_status": "MISSING_RESPONSE_OPERATOR"}),
        nonclaim({"prediction_id": "PRED2770_2_PPN_beta_source_weight", "arena": "PPN_Newton", "product_symbol": "P_PPN_source_weight_beta", "product_value": "MISSING_C_BETA_SOURCE_WEIGHT_PRODUCT", "product_units": "dimensionless", "required_inputs": "C_beta_source_weight;Delta_w_source;weak_field_response_map OR theorem-zero", "derivation_status": "MISSING_RESPONSE_OPERATOR"}),
        nonclaim({"prediction_id": "PRED2770_3_R10_relative_weight_lambda", "arena": "R10_short_range", "product_symbol": "P_R10_relative_weight(lambda)", "product_value": "MISSING_KW_DELTAW_SOURCE_DELTAW_TEST_TAU_R10_PRODUCT", "product_units": "dimensionless", "required_inputs": "lambda_w;K_w(lambda);Delta_w_source;Delta_w_test;tau_R10;alpha_bound(lambda) OR theorem-zero", "derivation_status": "MISSING_R10_RELATIVE_WEIGHT_PRODUCT"}),
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"bound_id": "BOUND2770_0_WEP_source_charge", "arena": "MICROSCOPE_WEP", "product_symbol": "P_WEP_relative_source_weight", "bound_value": "2.8e-15", "bound_units": "dimensionless", "bound_type": "numeric_bound_nonclaim"}),
        nonclaim({"bound_id": "BOUND2770_1_PPN_gamma", "arena": "PPN_Newton", "product_symbol": "P_PPN_source_weight_gamma", "bound_value": "2.3e-05", "bound_units": "dimensionless", "bound_type": "numeric_bound_nonclaim"}),
        nonclaim({"bound_id": "BOUND2770_2_PPN_beta", "arena": "PPN_Newton", "product_symbol": "P_PPN_source_weight_beta", "bound_value": "7.8e-05", "bound_units": "dimensionless", "bound_type": "numeric_bound_nonclaim"}),
        nonclaim({"bound_id": "BOUND2770_3_R10_alpha_lambda", "arena": "R10_short_range", "product_symbol": "P_R10_relative_weight(lambda)", "bound_value": "MISSING_PROMOTED_ALPHA_LAMBDA_CURVE", "bound_units": "range-dependent", "bound_type": "symbolic_curve_required"}),
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
        if row.get("valid_for_claim") is True
        and is_numeric(row.get("product_value"))
        and not has_missing_marker(row)
    ]
    valid_bounds = [
        row for row in bounds
        if is_numeric(row.get("bound_value"))
        and float(str(row["bound_value"])) > 0.0
        and not has_missing_marker(row)
    ]
    comparisons = [nonclaim({"comparison_id": "PRODUCT_COMPARE_NO_VALID_PREDICTIONS", "arena": "", "product_symbol": "", "product_value": "", "bound_value": "", "comparison_status": "not_run", "pass_for_claim": False, "issues": "no valid MTS relative-weight product prediction rows"})]
    runner = [nonclaim({"runner_id": "APR2770_0_relative_weight_product_runner", "prediction_rows": len(predictions), "bound_rows": len(bounds), "valid_prediction_rows": len(valid_predictions), "valid_bound_rows": len(valid_bounds), "comparison_rows": len(comparisons), "claim_allowed": False, "expected_result": "reject_all_relative_weight_placeholders"})]
    return runner, comparisons


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CG2770_0_source_label_forgetting", "claim": "source-label forgetting is derived", "gate_pass": False, "reason": "conditional theorem exists but the parent category has not removed labels before source selection", "claim_allowed": False}),
        nonclaim({"row_id": "CG2770_1_Noether_current_owner", "claim": "Noether/current owner fixes source normalization", "gate_pass": False, "reason": "PIC989_2 remains candidate_missing and ELA989_2 remains unsigned", "claim_allowed": False}),
        nonclaim({"row_id": "CG2770_2_relative_weights_zero", "claim": "relative source weights vanish", "gate_pass": False, "reason": "w_A counterexample survives same-action/additivity unless parent minimality is derived", "claim_allowed": False}),
        nonclaim({"row_id": "CG2770_3_WEP_PPN_R10_scores", "claim": "relative-weight products score WEP/PPN/R10", "gate_pass": False, "reason": "all prediction products are placeholders and product runner has valid_prediction_rows=0", "claim_allowed": False}),
        nonclaim({"row_id": "CG2770_4_local_GR_Newton", "claim": "local GR/Newton follows from source coupling", "gate_pass": False, "reason": "source coupling is one required gate; EH/R11/operator/PPN readout remain open", "claim_allowed": False}),
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "DEC2770_0_theorem_status", "decision": "source-label forgetting is a clean conditional theorem but not current derivation", "because": "labels must be removed before source coupling selection; current corpus has not signed that category step", "next_action": "keep theorem as parent-action contract"}),
        nonclaim({"row_id": "DEC2770_1_counterexample_status", "decision": "relative source weights are retained as explicit coupling debts", "because": "w_A survives covariance, Ward/additivity, and same-action rhetoric when parent minimality is unsigned", "next_action": "use product templates for WEP/PPN/R10 rather than hiding the coupling"}),
        nonclaim({"row_id": "DEC2770_2_best_next", "decision": "next target is parent category label-forgetting proof or relative-weight runner fill", "because": "this is the least hand-wavy route to universal coupling and measured-G source normalization", "next_action": "2771-Y5-R2FR-parent-category-label-forgetting-proof-or-relative-weight-runner-fill-under-AX1090.md"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2770_0_2771",
            "next_target": "2771-Y5-R2FR-parent-category-label-forgetting-proof-or-relative-weight-runner-fill-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_category_label_forgetting_proof_or_relative_weight_runner_fill_under_AX1090_2771.py",
            "why": "2770 localizes the universal-coupling obstruction to source labels, missing Noether/current owner, and relative source weights",
            "include": "category-domain proof attempt, no-source-only-slot theorem, w_A prior-width requirements, WEP/PPN/Gdot/R10 product runner schema, measured-G common-mode guard",
            "exclude": "assuming WEP, absorbing relative weights into G, unity shortcuts, cancellation, public local-GR/WEP/R10 claim, GitHub action, formalization-workbench edits",
        })
    ]


def copy_branch_outputs(
    theorem: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    prior: list[dict[str, Any]],
    template: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    theorem_rows = theorem + owner
    prior_rows = prior + template + gates
    beta_rows = owner + prior + next_rows
    microscope_rows = [row for row in prior + template if "WEP" in str(row.get("observable_channel", row.get("arena", "")))] + gates + next_rows
    specs = [
        ("BR2770_0_theorem_queue", "theorem", theorem_rows, OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_queue"], "source-label/Noether theorem attempt"),
        ("BR2770_1_prior_queue", "prior", prior_rows, OUTPUTS["prior"], BRANCH_OUTPUTS["prior_queue"], "relative-weight prior/product matrix"),
        ("BR2770_2_beta_doc", "beta_doc", beta_rows, OUTPUTS["owner"], BRANCH_OUTPUTS["beta_doc"], "beta/source-facing source-label copy"),
        ("BR2770_3_microscope_copy", "microscope", microscope_rows, OUTPUTS["template"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE relative-weight copy"),
        ("BR2770_4_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next parent-category label-forgetting target"),
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
    theorem = rows_by_name["theorem"]
    owner = rows_by_name["owner"]
    prior = rows_by_name["prior"]
    template = rows_by_name["template"]
    bounds = rows_by_name["bounds"]
    runner = rows_by_name["runner"]
    gates = rows_by_name["gates"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2770_0_sources", all(row["exists"] and row["needles_found"] for row in sources), "every cited source path exists and needles are found"),
        ("VAL2770_1_theorem_not_promoted", any(row["row_id"] == "THM2770_5_verdict" and row["attempt_result"] == "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED" for row in theorem), "source-label theorem is conditional and not promoted"),
        ("VAL2770_2_Noether_owner_missing", any(row["row_id"] == "NO2770_2_Noether_current_owner" and row["current_status"] == "candidate_missing" for row in owner), "Noether/current owner remains missing"),
        ("VAL2770_3_relative_weight_priors_written", all(any(row["row_id"] == required for row in prior) for required in ["RWP2770_1_delta_w_WEP", "RWP2770_2_delta_w_PPN", "RWP2770_3_delta_w_Gdot", "RWP2770_4_delta_w_R10"]), "relative-weight prior/debt rows cover WEP, PPN, Gdot, and R10 channels"),
        ("VAL2770_4_prediction_templates_nonclaim", all(row["valid_for_claim"] is False and has_missing_marker(row) for row in template), "all relative-weight prediction rows are missing-input placeholders"),
        ("VAL2770_5_bound_import_written", all(any(row["bound_id"] == required for row in bounds) for required in ["BOUND2770_0_WEP_source_charge", "BOUND2770_1_PPN_gamma", "BOUND2770_2_PPN_beta"]), "WEP and PPN numeric bound anchors are imported"),
        ("VAL2770_6_product_runner_refuses_placeholders", runner[0]["valid_prediction_rows"] == 0 and runner[0]["claim_allowed"] is False, "product runner refuses all relative-weight placeholders"),
        ("VAL2770_7_claim_gates_blocked", all(row["gate_pass"] is False and row["claim_allowed"] is False for row in gates), "all relative-weight and local-GR claim gates remain blocked"),
        ("VAL2770_8_next_target_written", any(row["row_id"] == "NEXT2770_0_2771" and "parent-category-label-forgetting" in row["next_target"] for row in next_rows), "next target selects parent-category label forgetting or relative-weight runner fill"),
        ("VAL2770_9_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2770_10_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2770_11_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2770_12_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2770_13_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2770_14_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({"validation_id": "VAL2770_OVERALL", "passed": all(row["passed"] for row in rows), "detail": "2770 ports the source-label forgetting and Noether/current owner audit into the current R2/f(R) branch, keeps universal coupling conditional, retains relative source weights as explicit WEP/PPN/Gdot/R10 product debts, refuses all placeholder products, and selects parent-category label-forgetting proof or relative-weight runner fill as the next target.", "timestamp_utc": ts()})
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2770 - Y5 R2/f(R): Source-Label Forgetting, Noether Current Owner, Or Relative-Weight Prior Under AX1090",
        "## Private Verdict\n\nThe universal-coupling theorem is clean but still conditional. The current corpus does not yet prove that the parent source functor forgets species labels before source coupling selection.\n\nCoupling wound: a constant relative source weight `w_A` survives covariance, Ward/additivity, and same-action language unless the parent category forbids source-only species slots.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "## Source-Forgetting Theorem Attempt\n\n" + markdown_table(rows_by_name["theorem"], ["row_id", "claim_shape", "formal_statement", "attempt_result", "why_it_matters", "current_gap", "valid_for_claim"]),
        "## Noether / Source Owner Audit\n\n" + markdown_table(rows_by_name["owner"], ["row_id", "object", "required_owner", "current_status", "if_missing", "source", "valid_for_claim"]),
        "## Relative-Weight Prior Matrix\n\n" + markdown_table(rows_by_name["prior"], ["row_id", "quantity", "definition", "observable_channel", "current_status", "required_for_claim", "bound_or_target", "valid_for_claim"]),
        "## Product Prediction Templates\n\n" + markdown_table(rows_by_name["template"], ["prediction_id", "arena", "product_symbol", "product_value", "product_units", "required_inputs", "derivation_status", "valid_for_claim"]),
        "## Bound Import\n\n" + markdown_table(rows_by_name["bounds"], ["bound_id", "arena", "product_symbol", "bound_value", "bound_units", "bound_type", "valid_for_claim"]),
        "## Product Runner Status\n\n" + markdown_table(rows_by_name["runner"], ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result", "valid_for_claim"]),
        "## Product Comparison Rows\n\n" + markdown_table(rows_by_name["comparisons"], ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["row_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision Ledger\n\n" + markdown_table(rows_by_name["decision"], ["row_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "why", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis is the GR/Newton source-coupling knot in plain clothes. If MTS can prove the parent source category forgets species labels, relative source weights die structurally. If not, they become explicit test products rather than something hidden in measured `G`.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    sources = build_sources()
    theorem = build_theorem_rows()
    owner = build_owner_rows()
    prior = build_prior_rows()
    template = build_prediction_rows()
    bounds = build_bound_rows()
    runner, comparisons = run_product_runner(template, bounds)
    gates = build_gates()
    decision = build_decision()
    next_rows = build_next()

    for key, rows in [
        ("sources", sources), ("theorem", theorem), ("owner", owner), ("prior", prior), ("template", template),
        ("bounds", bounds), ("runner", runner), ("comparisons", comparisons), ("gates", gates), ("decision", decision), ("next", next_rows)
    ]:
        write_csv(OUTPUTS[key], rows)

    branches = copy_branch_outputs(theorem, owner, prior, template, gates, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources, "theorem": theorem, "owner": owner, "prior": prior, "template": template,
        "bounds": bounds, "runner": runner, "comparisons": comparisons, "gates": gates, "decision": decision,
        "next": next_rows, "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2770_OVERALL")
    print(f"2770 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
