from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "793-Y5-R10-Gamma-Khat-balance-source-equation-or-local-bound-inputs.md"
NEXT_TARGET = "794-Y5-R10-tracefree-longitudinal-Khat-solver-or-PPN-bound.md"
STATUS = "Y5_R10_793_trace_piece_shortcut_blocked_tracefree_Khat_longitudinal_balance_route_defined_nonclaim"
CLAIM_CEILING = "Gamma_Khat_balance_audit_only_no_tracefree_solver_no_q_loc_zero_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_793_SOURCE_REGISTER.csv"
TRACE_STATUS_PATH = RESIDUALS / "P8_Y5_R10_793_KHAT_TRACE_STATUS_GATE.csv"
BALANCE_SOURCE_PATH = RESIDUALS / "P8_Y5_R10_793_GAMMA_KHAT_BALANCE_SOURCE_ROUTES.csv"
BOUND_INPUTS_PATH = RESIDUALS / "P8_Y5_R10_793_LOCAL_BOUND_INPUTS_IF_BALANCE_FAILS.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_793_DERIVATION_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_793_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_793_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_793_QLOC_ZERO_PROOF.csv",
    RESIDUALS / "P8_Y5_R10_793_KHAT_BALANCE_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_793_LOCAL_GR_PASS_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_793_PPN_BOUND_PASS_CERTIFICATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    TRACE_STATUS_PATH,
    BALANCE_SOURCE_PATH,
    BOUND_INPUTS_PATH,
    DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "792_doc": {
        "path": POST_CHECKPOINT / "792-Y5-R10-geometric-q-loc-cancellation-or-TMTS-residual-bound.md",
        "needles": ["Current result", "Gamma_eff/K_hat/P_loc"],
        "role": "immediate 793 handoff",
    },
    "792_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_792_VALIDATION.csv",
        "needles": ["V792_4_exact_balance_present", "V792_10_inputs_missing"],
        "role": "prior validation guard",
    },
    "792_cancellation": {
        "path": RESIDUALS / "P8_Y5_R10_792_QLOC_CANCELLATION_GATE.csv",
        "needles": ["QCG792_1_exact_balance", "QCG792_4_verdict"],
        "role": "q_loc cancellation route input",
    },
    "eq_register_05": {
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": ["K_MTS,mu_nu = -Gamma_eff g_mu_nu + K_hat,mu_nu", "trace-free residual"],
        "role": "trace-free K_hat status",
    },
    "ledger_14": {
        "path": FORMALIZATION / "14-field-definitions-dimensional-ledger.md",
        "needles": ["q_tr^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}", "[K_hat,mu_nu] = L^-2"],
        "role": "q_loc dimensional ledger",
    },
    "eq_register_balance": {
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": ["nabla^nu Gamma_eff", "nabla_mu K_hat^{mu nu}"],
        "role": "prior balance equation entries",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post_checkpoint(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for scanned_path in FORMALIZATION.rglob("*"):
        if scanned_path.is_file() and datetime.fromtimestamp(scanned_path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            changed_count += 1
    return changed_count


def validation_clean(number: int) -> bool:
    path = RESIDUALS / f"P8_Y5_BRR545_{number}_VALIDATION.csv"
    rows = read_csv_rows(path)
    return path.exists() and bool(rows) and all(row.get("result") == "pass" for row in rows)


def source_register_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCE_SPECS.items()
    ]


def trace_status_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "KTS793_0_existing_split",
            "statement": "K_MTS,mu_nu = -Gamma_eff g_mu_nu + K_hat,mu_nu",
            "implication": "Gamma_eff already owns the metric-proportional trace-like piece",
            "result": "source_confirmed",
            "effect_on_q_loc": "q_loc measures the mismatch between grad Gamma_eff and div K_hat",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "KTS793_1_tracefree_status",
            "statement": "K_hat is the trace-free residual after the metric-proportional part is separated",
            "implication": "the easy identity K_hat=Gamma_eff g is not allowed for the existing K_hat object",
            "result": "trace_shortcut_blocked",
            "effect_on_q_loc": "cancellation must come from trace-free divergence, not a hidden trace term",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "KTS793_2_dimensional_consistency",
            "statement": "[Gamma_eff]=[K_hat]=L^-2 and [q_loc]=L^-3",
            "implication": "a divergence balance is dimensionally consistent",
            "result": "pass_formal",
            "effect_on_q_loc": "no dimensional obstruction to div K_hat matching grad Gamma_eff",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "KTS793_3_degrees_of_freedom",
            "statement": "a symmetric trace-free K_hat in four dimensions has nine local components and four divergence equations",
            "implication": "a local trace-free divergence solver is plausible but nonunique",
            "result": "possible_not_derived",
            "effect_on_q_loc": "needs gauge/boundary/constitutive law to avoid arbitrary counterterm",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def balance_source_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "GBS793_0_trace_shortcut",
            "route": "put Gamma_eff g^{mu nu} into K_hat",
            "equation_or_condition": "K_hat^{mu nu}=Gamma_eff g^{mu nu} would give div K_hat = grad Gamma_eff by metric compatibility",
            "result": "rejected_for_existing_Khat",
            "why": "existing register defines K_hat as trace-free residual after the metric-proportional part is separated",
            "next_requirement": "do not use this as a proof unless K_hat definition is changed explicitly",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "GBS793_1_tracefree_longitudinal_solver",
            "route": "solve for trace-free longitudinal K_L^{mu nu}",
            "equation_or_condition": "K_L^{mu nu}=nabla^{(mu} A^{nu)} - (1/4)g^{mu nu}nabla_alpha A^alpha plus curvature terms chosen so div K_L = grad Gamma_eff",
            "result": "best_derivation_route",
            "why": "keeps K_hat trace-free while giving a mathematical route to div K_hat=grad Gamma_eff",
            "next_requirement": "derive A^nu/K_L from parent action or solve with controlled boundary data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "GBS793_2_variational_constraint",
            "route": "constraint multiplier enforcing div K_hat - grad Gamma_eff = kernel(P_loc)",
            "equation_or_condition": "S_constraint = integral lambda_nu P_loc(div K_hat - grad Gamma_eff)^nu",
            "result": "closure_candidate_not_adopted",
            "why": "would force q_loc=0 but risks adding the desired result by hand",
            "next_requirement": "derive multiplier/constraint from symmetry or conservation principle",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "GBS793_3_relaxation_fixed_point",
            "route": "local relaxation drives q_loc -> 0",
            "equation_or_condition": "D_tau K_hat^{mu nu} contains -delta ||P_loc(div K_hat-grad Gamma_eff)||^2 / delta K_hat_mu_nu",
            "result": "dynamical_candidate",
            "why": "could make q_loc=0 an attractor instead of an imposed constraint",
            "next_requirement": "show stability, locality, covariance, and no PPN transient residual",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "GBS793_4_bound_fallback",
            "route": "do not cancel; bound the residual",
            "equation_or_condition": "compute q_loc source profile and T_Q carrier response",
            "result": "fallback_retained",
            "why": "needed if source equations do not produce a clean cancellation theorem",
            "next_requirement": "PPN/orbital/clock/R10 response coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def bound_input_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "input_id": "LBI793_0_tracefree_solver_operator",
            "needed_input": "operator mapping A^nu or local potentials to trace-free K_L^{mu nu}",
            "why_needed": "turns the plausible trace-free divergence balance into an actual equation",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "LBI793_1_boundary_data",
            "needed_input": "local boundary conditions for A^nu/K_hat/T_Q",
            "why_needed": "divergence equations are nonunique and boundary-sensitive",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "LBI793_2_parent_action_origin",
            "needed_input": "action or symmetry producing the trace-free longitudinal solver",
            "why_needed": "prevents the solver from being a hand-tuned counterterm",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "LBI793_3_amplitude_bound",
            "needed_input": "norm bound on K_L and resulting Kbar_tr,loc,00",
            "why_needed": "even a cancelling divergence can carry local metric stress",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "input_id": "LBI793_4_observable_response",
            "needed_input": "PPN/orbital/clock/R10 response map for K_L/T_Q",
            "why_needed": "needed if cancellation is imperfect or has a carrier stress footprint",
            "status": "missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D793_0_trace_shortcut_blocked",
            "decision": "reject the simple K_hat=Gamma_eff g shortcut",
            "reason": "K_hat is already defined as trace-free residual",
            "result": "blocked_by_source_definition",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D793_1_tracefree_solver_selected",
            "decision": "try trace-free longitudinal K_hat solver next",
            "reason": "it is the least-cheaty route that can satisfy div K_hat=grad Gamma_eff without changing K_hat meaning",
            "result": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D793_2_no_q_zero_claim",
            "decision": "do not claim q_loc=0",
            "reason": "trace-free solver, boundary conditions, parent origin, and amplitude bounds are missing",
            "result": "claim_blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "the metric-trace shortcut is blocked because K_hat is trace-free; the best remaining derivation route is a trace-free longitudinal K_hat solver whose divergence matches grad Gamma_eff",
            "hard_blocker": "derive or bound the trace-free longitudinal solver, including boundary data, parent-action origin, and local PPN/metric footprint",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_rows(*row_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in row_groups:
        rows.extend(group)
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    trace: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_792_clean = all(validation_clean(number) for number in range(665, 793))
    trace_complete = len(trace) == 4
    trace_shortcut_blocked = any(row["gate_id"] == "KTS793_1_tracefree_status" and row["result"] == "trace_shortcut_blocked" for row in trace)
    dof_possible = any(row["gate_id"] == "KTS793_3_degrees_of_freedom" and row["result"] == "possible_not_derived" for row in trace)
    routes_complete = len(routes) == 5
    rejected_trace_route = any(row["route_id"] == "GBS793_0_trace_shortcut" and row["result"] == "rejected_for_existing_Khat" for row in routes)
    longitudinal_selected = any(row["route_id"] == "GBS793_1_tracefree_longitudinal_solver" and row["result"] == "best_derivation_route" for row in routes)
    inputs_complete = len(inputs) == 5
    inputs_missing = all(row["status"] == "missing" for row in inputs)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D793_1_tracefree_solver_selected" for row in decisions)
    no_claim = any(row["decision_id"] == "D793_2_no_q_zero_claim" and row["result"] == "claim_blocked" for row in decisions)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, trace, routes, inputs, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V793_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V793_1_source_needles_present", source_needles_present, "all source needles present"),
        ("V793_2_prior_665_792_clean", prior_665_792_clean, "665-792 validation rows have no failures"),
        ("V793_3_trace_status_complete", trace_complete, "K_hat trace-status rows complete"),
        ("V793_4_trace_shortcut_blocked", trace_shortcut_blocked, "metric-trace shortcut blocked by trace-free K_hat"),
        ("V793_5_degrees_possible", dof_possible, "trace-free divergence solver remains plausible"),
        ("V793_6_routes_complete", routes_complete, "Gamma/Khat balance source routes complete"),
        ("V793_7_rejected_trace_route", rejected_trace_route, "trace shortcut rejected"),
        ("V793_8_longitudinal_selected", longitudinal_selected, "trace-free longitudinal solver selected"),
        ("V793_9_inputs_complete", inputs_complete, "local bound/source inputs complete"),
        ("V793_10_inputs_missing", inputs_missing, "all solver/bound inputs still missing"),
        ("V793_11_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V793_12_no_claim", no_claim, "q_loc zero/local GR claim remains blocked"),
        ("V793_13_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V793_14_claim_artifacts_absent", claim_artifacts_absent, "no qloc/Khat/local-GR/PPN claim artifact fabricated"),
        ("V793_15_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V793_16_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V793_17_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    trace: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 793 - Y5 R10 Gamma Khat Balance Source Equation Or Local Bound Inputs

Current result: **the tempting trace shortcut is blocked by the existing theory definition**. Since `K_hat` is already the trace-free residual after the `Gamma_eff g` piece is separated, we cannot set `K_hat = Gamma_eff g` to kill `q_loc`. The viable route is subtler: construct a trace-free longitudinal `K_hat` component whose divergence matches `grad Gamma_eff`, then prove it comes from the parent action and does not create a PPN/local metric footprint.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Khat Trace Status Gate

{markdown_table(trace, ["gate_id", "statement", "implication", "result", "effect_on_q_loc", "valid_for_claim"])}

## Gamma Khat Balance Source Routes

{markdown_table(routes, ["route_id", "route", "equation_or_condition", "result", "why", "next_requirement", "valid_for_claim"])}

## Local Bound Inputs If Balance Fails

{markdown_table(inputs, ["input_id", "needed_input", "why_needed", "status", "valid_for_claim"])}

## Derivation Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is a proper correction: the easy cancellation would have cheated the existing definition of `K_hat`. The next honest route is a trace-free longitudinal solver. If that solver can be derived and its amplitude controlled, `q_loc` may be killed without redefining the theory. If it cannot, the local branch falls back to explicit PPN/orbital/clock/R10 bounds.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    trace = trace_status_rows(generated_utc)
    routes = balance_source_rows(generated_utc)
    inputs = bound_input_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, trace, routes, inputs, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(TRACE_STATUS_PATH, trace, ["gate_id", "statement", "implication", "result", "effect_on_q_loc", "valid_for_claim", "generated_utc"])
    write_csv(BALANCE_SOURCE_PATH, routes, ["route_id", "route", "equation_or_condition", "result", "why", "next_requirement", "valid_for_claim", "generated_utc"])
    write_csv(BOUND_INPUTS_PATH, inputs, ["input_id", "needed_input", "why_needed", "status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, trace, routes, inputs, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"793 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
