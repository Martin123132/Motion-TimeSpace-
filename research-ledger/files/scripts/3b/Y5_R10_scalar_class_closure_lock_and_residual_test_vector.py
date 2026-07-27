from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_scalar_class_closure_lock_and_residual_test_vector_written_nonclaim"
CLAIM_CEILING = "closure_assumed_residual_vector_only_no_parent_descent_no_theorem_zero_no_R10_PPN_WEP_Gdot_pass_no_local_GR_claim"
NEXT_TARGET = "713-Y5-R10-run-scalar-closure-residual-smoke-against-local-bound-baselines.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "712-Y5-R10-scalar-class-closure-lock-and-residual-test-vector.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_712_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_712_SCALAR_CLASS_CLOSURE_LOCK.csv",
    RESIDUALS / "P8_Y5_R10_712_SCALAR_CLASS_RESIDUAL_TEST_VECTOR.csv",
    RESIDUALS / "P8_Y5_R10_712_CLOSURE_VS_RETAINED_ROUTE.csv",
    RESIDUALS / "P8_Y5_R10_712_FORBIDDEN_PROMOTION_RULES.csv",
    RESIDUALS / "P8_Y5_R10_712_AEH_SCALAR_UPDATE.csv",
    RESIDUALS / "P8_Y5_R10_712_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_712_DECISION.csv",
    RESIDUALS / "P8_Y5_R10_712_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_712_VALIDATION.csv",
]

SOURCE_PATHS = {
    "711_doc": ROOT / "711-Y5-R10-derive-descent-clause-from-quotient-geometry-or-demote-scalar-zero-to-closure.md",
    "711_validation": RESIDUALS / "P8_Y5_BRR545_711_VALIDATION.csv",
    "711_demotion": RESIDUALS / "P8_Y5_R10_711_SCALAR_ZERO_DEMOTION_LEDGER.csv",
    "711_retained": RESIDUALS / "P8_Y5_R10_711_RETAINED_BRANCH_REQUIREMENTS.csv",
    "711_aeh": RESIDUALS / "P8_Y5_R10_711_AEH_SCALAR_UPDATE.csv",
    "710_descent": RESIDUALS / "P8_Y5_R10_710_DESCENT_PARENT_ACTION_CLAUSE.csv",
    "710_frame": RESIDUALS / "P8_Y5_R10_710_FRAME_TRANSFER_GUARD.csv",
    "708_r11": RESIDUALS / "P8_Y5_R10_708_R11_SCALAR_OPERATOR_ROW.csv",
    "708_r10": RESIDUALS / "P8_Y5_R10_708_R10_ALPHA_LAMBDA_SCALAR_TEMPLATE.csv",
    "local_template": RESIDUALS / "MTS_local_residual_predictions_TEMPLATE.csv",
    "r11_template": RESIDUALS / "R11_nonEH_operator_vector_TEMPLATE.csv",
    "r10_template": RESIDUALS / "R10_alpha_lambda_curve_TEMPLATE.csv",
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
        "711_doc": "scalar zero demotion predecessor",
        "711_validation": "711 validation gate",
        "711_demotion": "closure demotion rules",
        "711_retained": "retained branch requirements",
        "711_aeh": "closure-only AEH scalar update",
        "710_descent": "unowned descent clause target",
        "710_frame": "unowned frame guard target",
        "708_r11": "retained scalar R11 row",
        "708_r10": "retained scalar R10 template",
        "local_template": "canonical local residual prediction row shape",
        "r11_template": "canonical R11 non-EH operator vector template",
        "r10_template": "canonical R10 alpha(lambda) curve template",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": "true" if path.exists() else "false",
            "role": roles[source_id],
            "generated_utc": generated,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def closure_lock_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "SCL712_0_branch_identity",
            "branch_label",
            "MTS_scalar_class_silent_closure",
            "closure_assumed",
            "defines the only allowed name for scalar/class silence until parent descent is derived",
        ),
        (
            "SCL712_1_scope",
            "scope",
            "scalar/class contribution to local A_EH, source charge, R10, PPN, WEP, Gdot, and R11 rows",
            "closure_assumed",
            "does not silence other A_EH channels or full local-GR stack",
        ),
        (
            "SCL712_2_assumption",
            "closure assumption",
            "delta_AEH_scalar=0, grad_ln_AEH_scalar=0, q_Aa=0, alpha_AB(lambda)=0, scalar PPN/Gdot/WEP contribution=0",
            "closure_assumed",
            "testable branch value only",
        ),
        (
            "SCL712_3_parent_status",
            "parent derivation status",
            "not parent-derived; QDA711_2/QDA711_3/QDA711_4 failed",
            "blocked",
            "prevents theorem-zero promotion",
        ),
        (
            "SCL712_4_exit_to_theorem",
            "exit condition",
            "derive QDA711_0 through QDA711_7 and DPC710_0 through DPC710_7 with source paths and no MISSING markers",
            "not_satisfied",
            "only route from closure to theorem",
        ),
        (
            "SCL712_5_exit_to_retained",
            "retained branch condition",
            "if closure is rejected, use 708 R11/R10 scalar rows and source coefficients before scoring",
            "available_unfilled",
            "modified-gravity branch remains possible but unfilled",
        ),
        (
            "SCL712_6_verdict",
            "claim-ready status",
            "closure branch locked for testing but not valid for claim",
            "nonclaim_locked",
            "safe private test branch",
        ),
    ]
    return [
        {
            "lock_id": lock_id,
            "item": item,
            "value": value,
            "status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("711_doc", "711_demotion", "711_retained", "711_aeh"),
            "generated_utc": generated,
        }
        for lock_id, item, value, status, effect in rows
    ]


def residual_test_vector_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "MTS_scalar_class_silent_closure",
            "post_711_closure_lock",
            "SCV712_0_AEH_delta",
            "delta_AEH_scalar",
            "0",
            "",
            "0",
            "dimensionless",
            "closure_vector",
            "closure_assumed",
            "CLOSURE_ZERO_ONLY; not parent-derived",
            "scalar/class A_EH contribution only; other A_EH channels remain active",
        ),
        (
            "MTS_scalar_class_silent_closure",
            "post_711_closure_lock",
            "SCV712_1_AEH_gradient",
            "grad_ln_AEH_scalar",
            "0",
            "",
            "0",
            "per_length_or_per_time",
            "closure_vector",
            "closure_assumed",
            "CLOSURE_ZERO_ONLY; not parent-derived",
            "does not prove full kappa-gradient silence",
        ),
        (
            "MTS_scalar_class_silent_closure",
            "post_711_closure_lock",
            "R1_WEP_source_charge",
            "eta_WEP_source_charge_scalar",
            "0",
            "",
            "0",
            "dimensionless",
            "closure_vector",
            "closure_assumed",
            "matter blindness assumed only for scalar/class branch",
            "does not prove full WEP pass",
        ),
        (
            "MTS_scalar_class_silent_closure",
            "post_711_closure_lock",
            "R2_clock_redshift",
            "alpha_clock_redshift_scalar",
            "0",
            "",
            "0",
            "dimensionless",
            "closure_vector",
            "closure_assumed",
            "clock/readout independence assumed only for scalar/class branch",
            "does not prove EM/clock sector",
        ),
        (
            "MTS_scalar_class_silent_closure",
            "post_711_closure_lock",
            "R3_gamma",
            "gamma_minus_1_scalar",
            "0",
            "",
            "0",
            "dimensionless",
            "closure_vector",
            "closure_assumed",
            "scalar/class PPN slip contribution closed by assumption",
            "does not prove full gamma=1",
        ),
        (
            "MTS_scalar_class_silent_closure",
            "post_711_closure_lock",
            "R4_beta",
            "beta_minus_1_scalar",
            "0",
            "",
            "0",
            "dimensionless",
            "closure_vector",
            "closure_assumed",
            "scalar/class nonlinear source contribution closed by assumption",
            "does not prove full beta=1",
        ),
        (
            "MTS_scalar_class_silent_closure",
            "post_711_closure_lock",
            "R9_Gdot",
            "Gdot_over_G_scalar",
            "0",
            "",
            "0",
            "yr^-1",
            "closure_vector",
            "closure_assumed",
            "scalar/class A_EH time drift closed by assumption",
            "does not prove full Gdot silence",
        ),
        (
            "MTS_scalar_class_silent_closure",
            "post_711_closure_lock",
            "R10_fifth_force",
            "alpha_AB_lambda_scalar",
            "0",
            "",
            "0",
            "range-dependent",
            "closure_vector",
            "closure_assumed",
            "scalar charge q_Aa=0 assumed only for scalar/class branch",
            "does not count as R10 pass",
        ),
        (
            "MTS_scalar_class_silent_closure",
            "post_711_closure_lock",
            "R11_EH_operator_ledger",
            "scalar_tensor_class_metric",
            "0",
            "",
            "0",
            "operator family",
            "closure_vector",
            "closure_assumed",
            "operator retained row suppressed only in labelled closure branch",
            "R11 row remains available if closure rejected",
        ),
    ]
    fieldnames = [
        "model_id",
        "branch_id",
        "row_id",
        "observable",
        "predicted_value",
        "one_sigma",
        "upper_envelope",
        "units",
        "curve_or_vector_file",
        "derivation_status",
        "formula_reference",
        "assumptions",
    ]
    return [
        dict(zip(fieldnames, row))
        | {
            "source_file": str(DOC_PATH),
            "valid_for_claim": "false",
            "notes": "scalar/class closure test vector only; zero entries are not theorem-zero",
            "source_paths": source_list("local_template", "711_demotion", "711_retained", "711_aeh"),
            "generated_utc": generated,
        }
        for row in rows
    ]


def closure_vs_retained_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CVR712_0_delta", "delta_AEH_scalar", "closure_zero_only", "requires parent A_EH(u0) or zero theorem", "closure sets zero for branch testing; retained branch unfilled"),
        ("CVR712_1_gradient", "grad_ln_AEH_scalar", "closure_zero_only", "requires prefactor gradient/profile", "closure sets zero for branch testing; retained branch unfilled"),
        ("CVR712_2_charge", "q_Aa", "closure_zero_only", "requires matter charge vector or matter-blind theorem", "closure sets zero for branch testing; retained branch unfilled"),
        ("CVR712_3_R10", "alpha_AB(lambda)", "closure_zero_only", "requires lambda and alpha curve", "closure sets zero for branch testing; retained R10 template remains"),
        ("CVR712_4_PPN", "gamma/beta scalar contribution", "closure_zero_only", "requires scalar-tensor PPN map", "closure sets zero for branch testing; retained branch unfilled"),
        ("CVR712_5_R11", "scalar_tensor_class_metric", "closure_zero_only", "requires executable R11 coefficient row", "closure suppresses row only under label; retained R11 row remains"),
        ("CVR712_6_verdict", "route choice", "closure_locked_nonclaim", "retained branch requires real coefficients before scoring", "no route gives a claim yet"),
    ]
    return [
        {
            "route_id": route_id,
            "quantity": quantity,
            "closure_route_value": closure_value,
            "retained_route_requirement": retained_requirement,
            "policy": policy,
            "valid_for_claim": "false",
            "source_paths": source_list("708_r11", "708_r10", "711_retained", "711_aeh"),
            "generated_utc": generated,
        }
        for route_id, quantity, closure_value, retained_requirement, policy in rows
    ]


def forbidden_promotion_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("FPR712_0_no_theorem_zero", "Do not write derived_zero for scalar/class closure rows", "use closure_assumed until parent descent is proved"),
        ("FPR712_1_no_local_GR", "Do not use scalar closure to claim local GR", "other A_EH, source-normalization, frame, boundary, and operator channels remain open"),
        ("FPR712_2_no_R10_pass", "Do not count alpha=0 closure as R10 pass", "R10 pass requires parent-derived charge zero or real alpha(lambda) comparison"),
        ("FPR712_3_no_PPN_pass", "Do not count scalar PPN zero as gamma/beta pass", "full PPN vector still needs all sectors"),
        ("FPR712_4_no_WEP_pass", "Do not count scalar matter-blind closure as WEP pass", "species/source universality remains wider than scalar/class branch"),
        ("FPR712_5_no_Gdot_pass", "Do not count scalar A_EH drift zero as Gdot pass", "source normalization and other prefactor channels remain active"),
        ("FPR712_6_no_public_claim", "Do not present closure vector as public evidence", "private test branch only"),
    ]
    return [
        {
            "rule_id": rule_id,
            "rule": rule,
            "enforcement": enforcement,
            "valid_for_claim": "false",
            "source_paths": source_list("711_demotion", "711_doc"),
            "generated_utc": generated,
        }
        for rule_id, rule, enforcement in rows
    ]


def aeh_update_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("AEHU712_0_delta_AEH_scalar", "delta_AEH_scalar", "0_IN_CLOSURE_BRANCH_ONLY", "closure_locked_nonclaim"),
        ("AEHU712_1_grad_ln_AEH_scalar", "grad_ln_AEH_scalar", "0_IN_CLOSURE_BRANCH_ONLY", "closure_locked_nonclaim"),
        ("AEHU712_2_q_Aa", "q_Aa", "0_IN_CLOSURE_BRANCH_ONLY", "closure_locked_nonclaim"),
        ("AEHU712_3_alpha_AB", "alpha_AB(lambda)", "0_IN_CLOSURE_BRANCH_ONLY", "closure_locked_nonclaim"),
        ("AEHU712_4_scalar_R11", "scalar_tensor_class_metric", "0_IN_CLOSURE_BRANCH_ONLY_OR_RETAINED_R11_IF_REJECTED", "closure_locked_nonclaim"),
        ("AEHU712_5_AEH_sum", "A_EH", "MISSING_OTHER_CHANNEL_VALUES_OR_ZERO_THEOREMS", "still_unfilled_after_712"),
    ]
    return [
        {
            "update_id": update_id,
            "target": target,
            "value_or_bound": value,
            "current_status": status,
            "valid_for_claim": "false",
            "source_paths": source_list("711_aeh", "711_demotion", "710_descent"),
            "generated_utc": generated,
        }
        for update_id, target, value, status in rows
    ]


def gate_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CG712_0_sources", "all source files load", "source register exists check", "pass_structure", "allows checkpoint only"),
        ("CG712_1_prior_711", "711 validation clean", "711 validation has no failures", "pass_structure", "inherits clean predecessor"),
        ("CG712_2_closure_lock", "closure branch label", "MTS_scalar_class_silent_closure locked", "pass_structure", "safe branch naming"),
        ("CG712_3_residual_vector", "closure residual vector", "zeros are closure_assumed not derived_zero", "pass_structure", "test vector only"),
        ("CG712_4_forbidden_promotions", "promotion guards", "rules written", "pass_structure", "prevents claim laundering"),
        ("CG712_5_parent_descent", "parent descent", "not derived", "fail_blocked", "no theorem-zero claim"),
        ("CG712_6_full_local_stack", "full local-GR stack", "not reached", "fail_blocked", "no local-GR claim"),
        ("CG712_7_next_test", "future smoke test", "queued", "pass_structure", "next branch test only"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("711_validation", "711_demotion", "local_template"),
            "generated_utc": generated,
        }
        for gate_id, gate, observed, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("D712_0_lock", "scalar closure branch", "locked_nonclaim", "branch label and scope are explicit", NEXT_TARGET),
        ("D712_1_vector", "residual test vector", "written_nonclaim", "closure zeros are machine-readable but not theorem-zero", NEXT_TARGET),
        ("D712_2_retained", "retained scalar route", "available_unfilled", "if closure is rejected, use R11/R10 templates with real coefficients", NEXT_TARGET),
        ("D712_3_next", "next target", "selected", "run scalar closure residual smoke against local bound baselines without claiming pass", NEXT_TARGET),
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


def summary_rows() -> list[dict[str, str]]:
    generated = now()
    return [
        {
            "summary_id": "S712_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "scalar/class silent closure branch is locked and represented as a nonclaim residual vector with closure_assumed zeros",
            "hardest_blocker": "parent descent remains unproved, so no closure zero may be promoted to theorem-zero or local-GR evidence",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def all_generated_rows(*groups: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for group in groups for row in group]


def validation_rows(source_rows, lock, vector, route, forbidden, aeh, gates, decisions, summary) -> list[dict[str, str]]:
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = len(validation_failures("711_validation"))
    lock_ok = any(row["lock_id"] == "SCL712_0_branch_identity" and row["value"] == "MTS_scalar_class_silent_closure" for row in lock)
    lock_nonclaim = all(row["valid_for_claim"] == "false" for row in lock)
    vector_rows_required = {
        "SCV712_0_AEH_delta",
        "SCV712_1_AEH_gradient",
        "R1_WEP_source_charge",
        "R2_clock_redshift",
        "R3_gamma",
        "R4_beta",
        "R9_Gdot",
        "R10_fifth_force",
        "R11_EH_operator_ledger",
    }
    vector_complete = vector_rows_required.issubset({row["row_id"] for row in vector})
    vector_closure_only = all(row["derivation_status"] == "closure_assumed" and row["valid_for_claim"] == "false" for row in vector)
    route_ok = any(row["route_id"] == "CVR712_6_verdict" and row["closure_route_value"] == "closure_locked_nonclaim" for row in route)
    forbidden_ok = len(forbidden) >= 7 and all(row["valid_for_claim"] == "false" for row in forbidden)
    aeh_closure_only = all(row["valid_for_claim"] == "false" for row in aeh) and any("IN_CLOSURE_BRANCH_ONLY" in row["value_or_bound"] for row in aeh)
    gates_block = all(row["valid_for_claim"] == "false" for row in gates) and any(row["result"] == "fail_blocked" for row in gates)
    no_claim = all(row.get("valid_for_claim") != "true" for row in all_generated_rows(lock, vector, route, forbidden, aeh, gates, decisions, summary))
    no_derived_zero = all(row.get("derivation_status") != "derived_zero" for row in vector)
    next_selected = decisions[-1]["next_action"] == NEXT_TARGET and summary[0]["next_target"] == NEXT_TARGET
    scoped = all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_count()
    checks = [
        ("V712_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V712_1_prior_711_clean", prior_failures == 0, f"711_validation_failures={prior_failures}"),
        ("V712_2_closure_lock_label", lock_ok, "MTS_scalar_class_silent_closure"),
        ("V712_3_closure_lock_nonclaim", lock_nonclaim, f"lock_rows={len(lock)}"),
        ("V712_4_residual_vector_complete", vector_complete, f"vector_rows={len(vector)}"),
        ("V712_5_vector_closure_assumed_only", vector_closure_only, "all vector rows closure_assumed and nonclaim"),
        ("V712_6_no_derived_zero_rows", no_derived_zero, "no derived_zero rows in closure vector"),
        ("V712_7_closure_vs_retained_policy", route_ok, "closure locked; retained route still unfilled"),
        ("V712_8_forbidden_promotion_rules", forbidden_ok, f"rules={len(forbidden)}"),
        ("V712_9_AEH_update_closure_only", aeh_closure_only, "AEH scalar rows closure-only/nonclaim"),
        ("V712_10_gates_block_claim", gates_block, f"gate_rows={len(gates)}"),
        ("V712_11_no_claim_rows_promoted", no_claim, "all generated rows valid_for_claim=false"),
        ("V712_12_next_target_selected", next_selected, NEXT_TARGET),
        ("V712_13_outputs_scoped", scoped, "all outputs under post-checkpoint-work"),
        ("V712_14_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V712_15_status_nonclaim", "closure_assumed" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
    ]
    return [{"check_id": cid, "result": "pass" if ok else "fail", "detail": detail, "generated_utc": generated} for cid, ok, detail in checks]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(source_rows, lock, vector, route, forbidden, aeh, gates, decisions, summary, validation) -> None:
    doc = f"""# 712 - Y5 R10 Scalar Class Closure Lock And Residual Test Vector

## Verdict

712 locks the scalar/class silent branch as an explicit closure branch:

```text
branch_label = MTS_scalar_class_silent_closure
derivation_status = closure_assumed
valid_for_claim = false
```

The branch now has a machine-readable residual vector. Its scalar/class entries are set to zero **only inside the labelled closure branch**. They are not `derived_zero`, not a local-GR proof, not an R10/PPN/WEP/Gdot pass, and not public evidence.

If the closure is rejected, the scalar/class sector falls back to the retained 708 R11/R10 rows and needs real coefficients before scoring.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Scalar Class Closure Lock

{markdown_table(lock, ["lock_id", "item", "value", "status", "claim_effect", "valid_for_claim"])}

## Scalar Class Residual Test Vector

{markdown_table(vector, ["row_id", "observable", "predicted_value", "units", "derivation_status", "valid_for_claim", "notes"])}

## Closure Vs Retained Route

{markdown_table(route, ["route_id", "quantity", "closure_route_value", "retained_route_requirement", "policy", "valid_for_claim"])}

## Forbidden Promotion Rules

{markdown_table(forbidden, ["rule_id", "rule", "enforcement", "valid_for_claim"])}

## AEH Scalar Update

{markdown_table(aeh, ["update_id", "target", "value_or_bound", "current_status", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    lock = closure_lock_rows()
    vector = residual_test_vector_rows()
    route = closure_vs_retained_rows()
    forbidden = forbidden_promotion_rows()
    aeh = aeh_update_rows()
    gates = gate_rows()
    decisions = decision_rows()
    summary = summary_rows()
    validation = validation_rows(source_rows, lock, vector, route, forbidden, aeh, gates, decisions, summary)

    write_csv(OUTPUT_PATHS[1], source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(
        OUTPUT_PATHS[2],
        lock,
        ["lock_id", "item", "value", "status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[3],
        vector,
        [
            "model_id",
            "branch_id",
            "row_id",
            "observable",
            "predicted_value",
            "one_sigma",
            "upper_envelope",
            "units",
            "curve_or_vector_file",
            "derivation_status",
            "formula_reference",
            "source_file",
            "assumptions",
            "valid_for_claim",
            "notes",
            "source_paths",
            "generated_utc",
        ],
    )
    write_csv(
        OUTPUT_PATHS[4],
        route,
        ["route_id", "quantity", "closure_route_value", "retained_route_requirement", "policy", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[5],
        forbidden,
        ["rule_id", "rule", "enforcement", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[6],
        aeh,
        ["update_id", "target", "value_or_bound", "current_status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[7],
        gates,
        ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[8],
        decisions,
        ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUTPUT_PATHS[9],
        summary,
        ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(OUTPUT_PATHS[10], validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_rows, lock, vector, route, forbidden, aeh, gates, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"lock_rows={len(lock)}")
    print(f"vector_rows={len(vector)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
