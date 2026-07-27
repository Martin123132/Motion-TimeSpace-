from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_scalar_closure_residual_smoke_against_local_bound_baselines_nonclaim"
CLAIM_CEILING = "closure_smoke_only_no_theorem_zero_no_R10_PPN_WEP_Gdot_or_local_GR_claim"
NEXT_TARGET = "714-Y5-R10-scalar-closure-vs-retained-branch-decision-gate.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "713-Y5-R10-run-scalar-closure-residual-smoke-against-local-bound-baselines.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_713_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_713_LOCAL_BOUND_BASELINES.csv",
    RESIDUALS / "P8_Y5_R10_713_SCALAR_CLOSURE_BOUND_SMOKE.csv",
    RESIDUALS / "P8_Y5_R10_713_SCORE_POLICY_GUARD.csv",
    RESIDUALS / "P8_Y5_R10_713_AEH_SCALAR_UPDATE.csv",
    RESIDUALS / "P8_Y5_R10_713_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_713_DECISION.csv",
    RESIDUALS / "P8_Y5_R10_713_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_713_VALIDATION.csv",
]

SOURCE_PATHS = {
    "712_doc": ROOT / "712-Y5-R10-scalar-class-closure-lock-and-residual-test-vector.md",
    "712_validation": RESIDUALS / "P8_Y5_BRR545_712_VALIDATION.csv",
    "712_vector": RESIDUALS / "P8_Y5_R10_712_SCALAR_CLASS_RESIDUAL_TEST_VECTOR.csv",
    "712_rules": RESIDUALS / "P8_Y5_R10_712_FORBIDDEN_PROMOTION_RULES.csv",
    "712_route": RESIDUALS / "P8_Y5_R10_712_CLOSURE_VS_RETAINED_ROUTE.csv",
    "local_template": RESIDUALS / "MTS_local_residual_predictions_TEMPLATE.csv",
    "local_bound_register": RESIDUALS / "P8_LOCAL_GR_RESIDUAL_BOUND_REGISTER.csv",
    "ppn_vector": RESIDUALS / "P8_Y5_PPN_RESIDUAL_VECTOR.csv",
    "mu_scorecard": RESIDUALS / "P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv",
    "source_norm_scorecard": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
    "r10_contract": RESIDUALS / "P8_Y5_R10_BOUND_CURVE_REAL_DATA_CONTRACT.csv",
    "r10_template": RESIDUALS / "R10_alpha_lambda_curve_TEMPLATE.csv",
    "r11_template": RESIDUALS / "R11_nonEH_operator_vector_TEMPLATE.csv",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "missing", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate.is_file() and datetime.fromtimestamp(candidate.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    generated = now()
    roles = {
        "712_doc": "closure vector predecessor",
        "712_validation": "predecessor validation gate",
        "712_vector": "scalar/class closure residual vector",
        "712_rules": "forbidden promotion policy",
        "712_route": "closure versus retained route policy",
        "local_template": "canonical local residual row names",
        "local_bound_register": "existing local-GR residual/bound register",
        "ppn_vector": "gamma/beta PPN row guardrails",
        "mu_scorecard": "Gdot/gamma/beta local guardrails",
        "source_norm_scorecard": "source-normalization local guardrails",
        "r10_contract": "R10 real curve contract and blocked placeholders",
        "r10_template": "canonical alpha(lambda) curve row shape",
        "r11_template": "canonical R11 operator-family row shape",
        "655_doc": "R3/R4/R9/R10/R11 internal bound ledger",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": str(path.exists()).lower(),
            "role": roles[source_id],
            "generated_utc": generated,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def local_bound_baseline_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        {
            "baseline_id": "LBB713_0_AEH_delta",
            "target_row": "SCV712_0_AEH_delta",
            "observable": "delta_AEH_scalar",
            "bound_expression": "parent descent must set delta_AEH_scalar=0 or retained scalar coefficient must be sourced",
            "numeric_bound": "",
            "bound_units": "dimensionless",
            "bound_kind": "structural_parent_descent_gate",
            "comparison_policy": "not_scoreable_external_bound_missing",
            "source_paths": source_list("712_vector", "712_route", "655_doc"),
        },
        {
            "baseline_id": "LBB713_1_AEH_gradient",
            "target_row": "SCV712_1_AEH_gradient",
            "observable": "grad_ln_AEH_scalar",
            "bound_expression": "must map into Gdot/clock/PPN after length-time convention or be parent-derived zero",
            "numeric_bound": "",
            "bound_units": "per_length_or_per_time",
            "bound_kind": "structural_mapping_gate",
            "comparison_policy": "not_scoreable_units_projection_missing",
            "source_paths": source_list("712_vector", "source_norm_scorecard", "mu_scorecard"),
        },
        {
            "baseline_id": "LBB713_2_R1_WEP",
            "target_row": "R1_WEP_source_charge",
            "observable": "eta_WEP_source_charge_scalar",
            "bound_expression": "WEP/source-charge row requires species/source map; closure zero alone is not a WEP pass",
            "numeric_bound": "",
            "bound_units": "dimensionless",
            "bound_kind": "source_charge_mapping_gate",
            "comparison_policy": "not_scoreable_species_projection_missing",
            "source_paths": source_list("local_template", "712_rules", "source_norm_scorecard"),
        },
        {
            "baseline_id": "LBB713_3_R2_clock",
            "target_row": "R2_clock_redshift",
            "observable": "alpha_clock_redshift_scalar",
            "bound_expression": "clock/readout row requires observed metric/coframe map; closure zero alone is not a clock pass",
            "numeric_bound": "",
            "bound_units": "dimensionless",
            "bound_kind": "clock_readout_mapping_gate",
            "comparison_policy": "not_scoreable_clock_projection_missing",
            "source_paths": source_list("local_template", "712_rules", "source_norm_scorecard"),
        },
        {
            "baseline_id": "LBB713_4_R3_gamma",
            "target_row": "R3_gamma",
            "observable": "gamma_minus_1_scalar",
            "bound_expression": "abs(gamma_minus_1_scalar) <= 2.3e-05 dimensionless",
            "numeric_bound": "2.3e-05",
            "bound_units": "dimensionless",
            "bound_kind": "internal_ppn_guardrail",
            "comparison_policy": "numeric_smoke_only_closure_zero_not_evidence",
            "source_paths": source_list("ppn_vector", "mu_scorecard", "655_doc"),
        },
        {
            "baseline_id": "LBB713_5_R4_beta",
            "target_row": "R4_beta",
            "observable": "beta_minus_1_scalar",
            "bound_expression": "abs(beta_minus_1_scalar) <= 7.8e-05 dimensionless",
            "numeric_bound": "7.8e-05",
            "bound_units": "dimensionless",
            "bound_kind": "internal_ppn_guardrail",
            "comparison_policy": "numeric_smoke_only_closure_zero_not_evidence",
            "source_paths": source_list("ppn_vector", "mu_scorecard", "655_doc"),
        },
        {
            "baseline_id": "LBB713_6_R9_Gdot",
            "target_row": "R9_Gdot",
            "observable": "Gdot_over_G_scalar",
            "bound_expression": "abs(Gdot_over_G_scalar) <= 9.6e-15 yr^-1 if a time-drift channel is active",
            "numeric_bound": "9.6e-15",
            "bound_units": "yr^-1",
            "bound_kind": "contingent_internal_guardrail",
            "comparison_policy": "numeric_smoke_only_closure_zero_not_evidence",
            "source_paths": source_list("mu_scorecard", "source_norm_scorecard", "655_doc"),
        },
        {
            "baseline_id": "LBB713_7_R10_fifth_force",
            "target_row": "R10_fifth_force",
            "observable": "alpha_AB_lambda_scalar",
            "bound_expression": "requires real alpha_bound(lambda) curve or parent-derived q_Aa=0 theorem",
            "numeric_bound": "",
            "bound_units": "range-dependent",
            "bound_kind": "r10_curve_required",
            "comparison_policy": "not_scoreable_curve_missing_or_closure_zero_only",
            "source_paths": source_list("r10_contract", "r10_template", "712_rules"),
        },
        {
            "baseline_id": "LBB713_8_R11_operator",
            "target_row": "R11_EH_operator_ledger",
            "observable": "scalar_tensor_class_metric",
            "bound_expression": "requires executable R11 coefficient vector or EH-only theorem; closure suppresses only labelled scalar branch",
            "numeric_bound": "",
            "bound_units": "operator family",
            "bound_kind": "r11_operator_vector_required",
            "comparison_policy": "not_scoreable_operator_vector_missing_or_closure_only",
            "source_paths": source_list("r11_template", "712_route", "655_doc"),
        },
    ]
    for row in rows:
        row["source_status"] = "existing_internal_guardrail_or_contract"
        row["valid_for_claim"] = "false"
        row["generated_utc"] = generated
    return rows


def scalar_closure_bound_smoke_rows(vector_rows: list[dict[str, str]], baseline_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    generated = now()
    baseline_by_target = {row["target_row"]: row for row in baseline_rows}
    smoke_rows: list[dict[str, str]] = []
    for vector in vector_rows:
        row_id = vector["row_id"]
        baseline = baseline_by_target[row_id]
        predicted = float(vector["predicted_value"])
        numeric_bound = baseline["numeric_bound"]
        if numeric_bound:
            bound = float(numeric_bound)
            comparison_status = "within_bound_closure_only" if abs(predicted) <= bound else "outside_bound"
            normalized_abs_value = "0.0" if bound else ""
            margin_to_bound = f"{bound - abs(predicted):.12g}"
            smoke_detail = "numeric pipeline works, but the zero is closure_assumed and cannot become evidence"
        else:
            comparison_status = baseline["comparison_policy"]
            normalized_abs_value = ""
            margin_to_bound = ""
            smoke_detail = "not scoreable because the needed external curve, projection, or operator vector is missing"
        smoke_rows.append(
            {
                "smoke_id": f"SMK713_{len(smoke_rows)}_{row_id}",
                "source_vector_row": row_id,
                "observable": vector["observable"],
                "predicted_value": vector["predicted_value"],
                "predicted_units": vector["units"],
                "derivation_status": vector["derivation_status"],
                "baseline_id": baseline["baseline_id"],
                "bound_expression": baseline["bound_expression"],
                "numeric_bound": numeric_bound,
                "bound_units": baseline["bound_units"],
                "comparison_status": comparison_status,
                "normalized_abs_value": normalized_abs_value,
                "margin_to_bound": margin_to_bound,
                "claim_effect": "nonclaim_smoke_only",
                "valid_for_claim": "false",
                "source_paths": vector["source_paths"] + ";" + baseline["source_paths"],
                "notes": smoke_detail,
                "generated_utc": generated,
            }
        )
    return smoke_rows


def score_policy_guard_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "SPG713_0_closure_not_theorem",
            "closure_assumed zero is not derived_zero",
            "Any zero imported from 712 stays branch-labelled until parent descent is proved.",
            "blocks_theorem_zero_promotion",
        ),
        (
            "SPG713_1_numeric_smoke_not_evidence",
            "finite bound comparisons are pipeline checks only",
            "R3/R4/R9 zeros can be compared to numeric guardrails, but success is by assumption.",
            "blocks_PPN_Gdot_claim",
        ),
        (
            "SPG713_2_R10_curve_required",
            "R10 needs real alpha(lambda) curve or parent source-charge zero",
            "The current R10 row is alpha=0 closure-only and the real bound curve contract remains unfilled.",
            "blocks_R10_claim",
        ),
        (
            "SPG713_3_R11_vector_required",
            "R11 needs executable coefficient vector or EH-only theorem",
            "The scalar/class operator is silent only inside the closure branch.",
            "blocks_R11_claim",
        ),
        (
            "SPG713_4_local_stack_not_cleared",
            "scalar/class branch is not full local GR",
            "Other A_EH, source-normalization, frame, boundary, preferred-frame, and operator channels remain open.",
            "blocks_local_GR_claim",
        ),
        (
            "SPG713_5_retained_route_preserved",
            "closure rejection falls back to retained scalar R10/R11 branch",
            "If closure is not accepted, use 708/711 retained rows and source coefficients before scoring.",
            "keeps_modified_gravity_route_available",
        ),
    ]
    return [
        {
            "guard_id": guard_id,
            "rule": rule,
            "reason": reason,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("712_rules", "712_route", "r10_contract", "r11_template"),
            "generated_utc": generated,
        }
        for guard_id, rule, reason, effect in rows
    ]


def aeh_scalar_update_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "AEHU713_0_delta_AEH_scalar",
            "delta_AEH_scalar",
            "0_IN_CLOSURE_BRANCH_ONLY",
            "smoke_compared_to_structural_gate",
            "no theorem-zero; no full A_EH claim",
        ),
        (
            "AEHU713_1_grad_ln_AEH_scalar",
            "grad_ln_AEH_scalar",
            "0_IN_CLOSURE_BRANCH_ONLY",
            "smoke_compared_to_projection_gate",
            "no kappa/Gdot/clock claim",
        ),
        (
            "AEHU713_2_scalar_PPN",
            "gamma_minus_1_scalar;beta_minus_1_scalar",
            "0_IN_CLOSURE_BRANCH_ONLY",
            "numeric_guardrail_smoke_passes",
            "no PPN claim because parent descent is unproved",
        ),
        (
            "AEHU713_3_scalar_Gdot",
            "Gdot_over_G_scalar",
            "0_IN_CLOSURE_BRANCH_ONLY",
            "numeric_guardrail_smoke_passes",
            "no Gdot claim because zero is closure-assumed",
        ),
        (
            "AEHU713_4_scalar_R10_R11",
            "alpha_AB_lambda_scalar;scalar_tensor_class_metric",
            "0_IN_CLOSURE_BRANCH_ONLY_OR_RETAINED_BRANCH_IF_REJECTED",
            "not_scoreable",
            "R10 curve and R11 coefficient vector remain required",
        ),
    ]
    return [
        {
            "update_id": update_id,
            "target": target,
            "value_or_bound": value,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("712_vector", "712_route", "ppn_vector", "mu_scorecard", "r10_contract", "r11_template"),
            "generated_utc": generated,
        }
        for update_id, target, value, status, effect in rows
    ]


def claim_gate_rows(
    source_rows: list[dict[str, str]],
    vector_rows: list[dict[str, str]],
    baseline_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = validation_failures("712_validation")
    finite_smoke = [row for row in smoke_rows if row["numeric_bound"]]
    finite_ok = all(row["comparison_status"] == "within_bound_closure_only" for row in finite_smoke)
    not_scoreable = [row for row in smoke_rows if not row["numeric_bound"]]
    closure_ok = all(row["derivation_status"] == "closure_assumed" for row in vector_rows)
    rows = [
        (
            "CG713_0_sources",
            "all source files load",
            "missing_sources=" + str(len(missing_sources)),
            "pass_structure" if not missing_sources else "fail_blocked",
            "allows checkpoint only",
        ),
        (
            "CG713_1_prior_712",
            "712 validation clean",
            "712_validation_failures=" + str(len(prior_failures)),
            "pass_structure" if not prior_failures else "fail_blocked",
            "inherits clean closure vector",
        ),
        (
            "CG713_2_vector",
            "closure vector rows",
            f"rows={len(vector_rows)} closure_assumed={closure_ok}",
            "pass_structure" if len(vector_rows) == 9 and closure_ok else "fail_blocked",
            "input vector usable for smoke only",
        ),
        (
            "CG713_3_baselines",
            "local baseline rows",
            f"rows={len(baseline_rows)} numeric_rows={len([row for row in baseline_rows if row['numeric_bound']])}",
            "pass_structure" if len(baseline_rows) == len(vector_rows) else "fail_blocked",
            "baseline map explicit",
        ),
        (
            "CG713_4_numeric_smoke",
            "finite numeric guardrail comparison",
            f"finite_rows={len(finite_smoke)} within_bound={finite_ok}",
            "pass_smoke" if finite_ok else "fail_blocked",
            "format works only; no evidence promotion",
        ),
        (
            "CG713_5_unscoreable_rows",
            "non-finite/projection rows",
            "not_scoreable_rows=" + str(len(not_scoreable)),
            "pass_blocked_recorded" if not_scoreable else "fail_blocked",
            "R1/R2/R10/R11/projection gates stay blocked",
        ),
        (
            "CG713_6_R10",
            "R10 fifth-force branch",
            "real alpha(lambda) curve or parent q_Aa zero theorem missing",
            "fail_blocked",
            "no R10 claim",
        ),
        (
            "CG713_7_R11",
            "R11 scalar/class operator branch",
            "executable coefficient vector or EH-only theorem missing",
            "fail_blocked",
            "no R11/local-GR claim",
        ),
        (
            "CG713_8_parent_descent",
            "parent descent theorem",
            "not derived; closure remains assumption",
            "fail_blocked",
            "no theorem-zero claim",
        ),
        (
            "CG713_9_nonclaim",
            "no rows promoted",
            "all generated rows valid_for_claim=false",
            "pass_structure",
            "claim laundering blocked",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": state,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("712_validation", "712_vector", "local_bound_register", "ppn_vector", "mu_scorecard", "r10_contract", "r11_template"),
            "generated_utc": generated,
        }
        for gate_id, gate, state, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "D713_0_smoke",
            "scalar closure residual smoke",
            "completed_nonclaim",
            "finite R3/R4/R9 rows compare cleanly only because the branch assumes zero",
            NEXT_TARGET,
        ),
        (
            "D713_1_R10",
            "R10 scalar closure row",
            "blocked_for_claim",
            "alpha_AB(lambda)=0 is closure-only; real curve or parent charge-zero theorem still required",
            NEXT_TARGET,
        ),
        (
            "D713_2_R11",
            "R11 scalar/class row",
            "blocked_for_claim",
            "operator family is silent only by branch label; executable vector or EH-only theorem still required",
            NEXT_TARGET,
        ),
        (
            "D713_3_next",
            "next target",
            "selected",
            "decide whether scalar closure is an allowed local-stack closure or force retained scalar coefficient sourcing",
            NEXT_TARGET,
        ),
    ]
    return [
        {
            "decision_id": decision_id,
            "target": target,
            "result": result,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
        for decision_id, target, result, reason, next_action in rows
    ]


def all_generated_rows(*tables: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for table in tables:
        rows.extend(table)
    return rows


def validation_rows(
    source_rows: list[dict[str, str]],
    vector_rows: list[dict[str, str]],
    baseline_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    guard_rows: list[dict[str, str]],
    aeh_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    generated = now()
    missing_sources = [row for row in source_rows if row["exists"] != "true"]
    prior_failures = validation_failures("712_validation")
    numeric_baselines = [row for row in baseline_rows if row["numeric_bound"]]
    finite_smoke = [row for row in smoke_rows if row["numeric_bound"]]
    nonnumeric_smoke = [row for row in smoke_rows if not row["numeric_bound"]]
    all_rows = all_generated_rows(
        source_rows,
        baseline_rows,
        smoke_rows,
        guard_rows,
        aeh_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
    )
    changed_count = formalization_changed_count()
    checks = [
        (
            "V713_0_source_paths_exist",
            not missing_sources,
            "all cited source paths exist" if not missing_sources else "missing=" + ",".join(row["source_id"] for row in missing_sources),
        ),
        (
            "V713_1_prior_712_clean",
            not prior_failures,
            "712_validation_failures=" + str(len(prior_failures)),
        ),
        (
            "V713_2_closure_vector_loaded",
            len(vector_rows) == 9,
            f"vector_rows={len(vector_rows)}",
        ),
        (
            "V713_3_vector_closure_assumed_only",
            all(row["derivation_status"] == "closure_assumed" and row["valid_for_claim"] == "false" for row in vector_rows),
            "all vector rows closure_assumed and nonclaim",
        ),
        (
            "V713_4_no_derived_zero_inputs",
            all(row["derivation_status"] != "derived_zero" for row in vector_rows),
            "no derived_zero rows in scalar closure vector",
        ),
        (
            "V713_5_baseline_map_complete",
            {row["target_row"] for row in baseline_rows} == {row["row_id"] for row in vector_rows},
            f"baseline_rows={len(baseline_rows)}",
        ),
        (
            "V713_6_numeric_bound_rows_parse",
            all(float(row["numeric_bound"]) > 0 for row in numeric_baselines),
            f"numeric_baselines={len(numeric_baselines)}",
        ),
        (
            "V713_7_numeric_smoke_within_bound",
            all(row["comparison_status"] == "within_bound_closure_only" for row in finite_smoke),
            f"finite_smoke_rows={len(finite_smoke)}",
        ),
        (
            "V713_8_nonscoreable_rows_blocked",
            all("not_scoreable" in row["comparison_status"] for row in nonnumeric_smoke),
            f"nonscoreable_rows={len(nonnumeric_smoke)}",
        ),
        (
            "V713_9_R10_R11_blocked",
            any(row["gate_id"] == "CG713_6_R10" and row["result"] == "fail_blocked" for row in gate_rows)
            and any(row["gate_id"] == "CG713_7_R11" and row["result"] == "fail_blocked" for row in gate_rows),
            "R10 and R11 claim gates remain blocked",
        ),
        (
            "V713_10_policy_guards_written",
            len(guard_rows) == 6,
            f"guards={len(guard_rows)}",
        ),
        (
            "V713_11_AEH_update_nonclaim",
            len(aeh_rows) == 5 and all(row["valid_for_claim"] == "false" for row in aeh_rows),
            f"aeh_rows={len(aeh_rows)}",
        ),
        (
            "V713_12_no_claim_rows_promoted",
            all(row.get("valid_for_claim", "false") == "false" for row in all_rows),
            "all generated rows valid_for_claim=false",
        ),
        (
            "V713_13_next_target_selected",
            any(row["next_action"] == NEXT_TARGET for row in decision_rows_),
            NEXT_TARGET,
        ),
        (
            "V713_14_outputs_scoped",
            all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS),
            "all outputs under post-checkpoint-work",
        ),
        (
            "V713_15_formalization_workbench_untouched",
            changed_count == 0,
            f"formalization_changed_after_cutoff={changed_count}",
        ),
        (
            "V713_16_status_nonclaim",
            CLAIM_CEILING in summary_rows[0]["claim_ceiling"],
            CLAIM_CEILING,
        ),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": generated,
        }
        for check_id, passed, detail in checks
    ]


def nonclaim_summary_rows(smoke_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    generated = now()
    finite_rows = [row for row in smoke_rows if row["numeric_bound"]]
    blocked_rows = [row for row in smoke_rows if not row["numeric_bound"]]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "finite_smoke_rows": str(len(finite_rows)),
            "blocked_or_projection_rows": str(len(blocked_rows)),
            "main_result": "scalar closure residual vector is machine-comparable against selected local baselines, but only as a nonclaim branch smoke test",
            "remaining_blocker": "parent descent or retained scalar coefficients; R10 curve and R11 operator vector remain unfilled",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def write_markdown(
    source_rows: list[dict[str, str]],
    baseline_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    guard_rows: list[dict[str, str]],
    aeh_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    content = f"""# 713 - Y5 R10 Run Scalar Closure Residual Smoke Against Local Bound Baselines

## Summary

713 runs the 712 scalar/class closure vector against the existing local-bound baseline ledgers as a private smoke test.

The important result is deliberately modest: the finite numeric rows `R3_gamma`, `R4_beta`, and `R9_Gdot` compare cleanly because the closure branch assumes their scalar/class contribution is zero. That is a pipeline/format check only. It is not a theorem-zero, not an R10 pass, not a PPN pass, not a Gdot pass, not an R11 pass, and not local-GR recovery.

| Status | `{STATUS}` |
| --- | --- |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Local Bound Baselines

{markdown_table(baseline_rows, ["baseline_id", "target_row", "observable", "bound_expression", "numeric_bound", "bound_units", "comparison_policy", "valid_for_claim"])}

## Scalar Closure Bound Smoke

{markdown_table(smoke_rows, ["smoke_id", "source_vector_row", "observable", "predicted_value", "numeric_bound", "bound_units", "comparison_status", "claim_effect", "valid_for_claim"])}

## Score Policy Guard

{markdown_table(guard_rows, ["guard_id", "rule", "claim_effect", "valid_for_claim"])}

## Aeh Scalar Update

{markdown_table(aeh_rows, ["update_id", "target", "value_or_bound", "current_status", "claim_effect", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gate_rows, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "finite_smoke_rows", "blocked_or_projection_rows", "main_result", "remaining_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Validation

{markdown_table(validation_rows_, ["check_id", "result", "detail"])}

## Verdict

The closure branch is now smoke-testable against local baselines, but it remains closure-only. The useful progress is not that it passes local gravity; it is that the branch cannot accidentally launder a closure assumption into evidence. Next we should decide whether to parent-sign the closure or demote it and build the retained scalar coefficient/source row.
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> int:
    source_rows = source_register_rows()
    vector_rows = read_csv(SOURCE_PATHS["712_vector"])
    baseline_rows = local_bound_baseline_rows()
    smoke_rows = scalar_closure_bound_smoke_rows(vector_rows, baseline_rows)
    guard_rows = score_policy_guard_rows()
    aeh_rows = aeh_scalar_update_rows()
    gate_rows = claim_gate_rows(source_rows, vector_rows, baseline_rows, smoke_rows)
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows(smoke_rows)
    validation_rows_ = validation_rows(
        source_rows,
        vector_rows,
        baseline_rows,
        smoke_rows,
        guard_rows,
        aeh_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
    )

    write_csv(
        RESIDUALS / "P8_Y5_R10_713_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "path", "exists", "role", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_713_LOCAL_BOUND_BASELINES.csv",
        baseline_rows,
        [
            "baseline_id",
            "target_row",
            "observable",
            "bound_expression",
            "numeric_bound",
            "bound_units",
            "bound_kind",
            "comparison_policy",
            "source_status",
            "source_paths",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_713_SCALAR_CLOSURE_BOUND_SMOKE.csv",
        smoke_rows,
        [
            "smoke_id",
            "source_vector_row",
            "observable",
            "predicted_value",
            "predicted_units",
            "derivation_status",
            "baseline_id",
            "bound_expression",
            "numeric_bound",
            "bound_units",
            "comparison_status",
            "normalized_abs_value",
            "margin_to_bound",
            "claim_effect",
            "valid_for_claim",
            "source_paths",
            "notes",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_713_SCORE_POLICY_GUARD.csv",
        guard_rows,
        ["guard_id", "rule", "reason", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_713_AEH_SCALAR_UPDATE.csv",
        aeh_rows,
        ["update_id", "target", "value_or_bound", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_713_CLAIM_GATE_EVALUATION.csv",
        gate_rows,
        ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_713_DECISION.csv",
        decision_rows_,
        ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_713_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "finite_smoke_rows",
            "blocked_or_projection_rows",
            "main_result",
            "remaining_blocker",
            "next_target",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_BRR545_713_VALIDATION.csv",
        validation_rows_,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_markdown(
        source_rows,
        baseline_rows,
        smoke_rows,
        guard_rows,
        aeh_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
        validation_rows_,
    )

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"{STATUS}: validation_passes={len(validation_rows_) - len(failures)}/{len(validation_rows_)}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
