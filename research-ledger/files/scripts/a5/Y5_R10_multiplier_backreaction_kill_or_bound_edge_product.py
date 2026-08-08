from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

DOC_PATH = ROOT / "588-Y5-R10-multiplier-backreaction-kill-or-bound-edge-product.md"

PRIOR_587_VALIDATION = RESIDUALS / "P8_Y5_BRR545_587_VALIDATION.csv"
PRIOR_587_EDGE_TARGETS = RESIDUALS / "P8_Y5_R10_587_EDGE_PRIOR_TIGHTENED_TARGETS.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_588_SOURCE_REGISTER.csv"
ADJOINT_THEOREM_PATH = RESIDUALS / "P8_Y5_R10_588_ADJOINT_BACKREACTION_THEOREM.csv"
KILL_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_588_BACKREACTION_KILL_ATTEMPT.csv"
CONSTRAINT_IDENTITY_PATH = RESIDUALS / "P8_Y5_R10_588_CONSTRAINT_IDENTITY_OR_NEW_EQUATION_GATE.csv"
EDGE_BUDGET_PATH = RESIDUALS / "P8_Y5_R10_588_EDGE_PRODUCT_FACTOR_BUDGET.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_588_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_588_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_588_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_588_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_multiplier_backreaction_kill_theorem_written_conditions_unfilled_edge_product_budgeted_nonclaim"
CLAIM_CEILING = "adjoint_zero_mode_theorem_contract_and_edge_product_budget_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "589-Y5-R10-adjoint-zero-mode-certificate-or-source-backed-edge-product-row.md"

SOURCE_FILES = [
    ("587-Y5-R10-affine-Vdef-parent-source-map-or-edge-prior-tightening.md", "immediate backreaction blocker handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_587_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_587_PARENT_SOURCE_EQUATION_CONTRACT.csv", "multiplier variation equations"),
    ("source-intake/mts_residuals/P8_Y5_R10_587_MULTIPLIER_NO_BACKREACTION_TEST.csv", "no-backreaction blockers"),
    ("source-intake/mts_residuals/P8_Y5_R10_587_EDGE_PRIOR_TIGHTENED_TARGETS.csv", "edge product pressure targets"),
    ("source-intake/mts_residuals/P8_Y5_R10_587_AFFINE_PARENT_SOURCE_MAP.csv", "affine ingredient source map"),
    ("586-Y5-R10-Vdef-owner-action-sketch-or-edge-runner-numeric-priors.md", "affine Vdef zero-Hessian contract"),
    ("583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md", "momentum-map owner and edge residual fork"),
    ("581-Y5-R10-quotient-vertical-no-pole-parent-theorem-attempt.md", "quotient vertical no-pole theorem shape"),
    ("513-Gamma-Khat-q_loc-first-variation-or-demotion.md", "q_loc Ward/stress-divergence route"),
    ("539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md", "Hamiltonian Pi_M projection branch"),
    ("scripts/Y5_R10_multiplier_backreaction_kill_or_bound_edge_product.py", "this checkpoint generator"),
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values: list[str] = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register() -> list[dict[str, Any]]:
    return [
        {"source_file": source_file, "exists": str((ROOT / source_file).exists()), "role": role}
        for source_file, role in SOURCE_FILES
    ]


def make_adjoint_theorem() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "ABT588_0_multiplier_variation",
            "mathematical_statement": "For S=S0[Y]+<X,C[Y]>, the field equations are E0_i[Y]+(DC[Y])^dagger_{i nu}X^nu=0 and C_nu[Y]=0.",
            "what_it_buys": "identifies the exact backreaction term rather than handwaving it away",
            "required_input": "explicit Frechet derivative DC and boundary pairing defining the adjoint",
            "current_status": "derived_as_formal_variation",
            "valid_for_claim": "false",
        },
        {
            "step_id": "ABT588_1_constraint_not_new_dynamics",
            "mathematical_statement": "C[Y]=0 must be a Noether/Bianchi identity on the local EH branch, or a first-class gauge constraint, not an extra equation selecting sources.",
            "what_it_buys": "prevents the multiplier from overconstraining GR-like local solutions",
            "required_input": "C=N(E0) or i_v Omega=delta G with first-class closure",
            "current_status": "not_derived",
            "valid_for_claim": "false",
        },
        {
            "step_id": "ABT588_2_adjoint_zero_mode_kill",
            "mathematical_statement": "If (DC)^dagger X=0 with proper/reference boundary conditions implies X=0, then delta_Y S_X vanishes on the local branch.",
            "what_it_buys": "kills multiplier backreaction without merely setting X=0 by taste",
            "required_input": "no-adjoint-zero-mode theorem or coercive estimate ||(DC)^dagger X||^2 >= m_adj^2 ||X||^2",
            "current_status": "contract_written_not_proved",
            "valid_for_claim": "false",
        },
        {
            "step_id": "ABT588_3_boundary_silence",
            "mathematical_statement": "The boundary pairing must vanish: <X,B_C[delta Y]>_boundary + <delta X,B_X>_boundary + delta S_boundary=0 or exact/proper-gauge.",
            "what_it_buys": "prevents edge hair after the bulk adjoint mode is killed",
            "required_input": "explicit B_X, B_C, reference subtraction, and allowed boundary data",
            "current_status": "not_derived",
            "valid_for_claim": "false",
        },
        {
            "step_id": "ABT588_4_matter_quotient",
            "mathematical_statement": "delta_X S_matter=0 and delta_Y S_matter uses the same observed quotient metric before any readout fit.",
            "what_it_buys": "kills qbar_XT and WEP leakage",
            "required_input": "parent quotient map pi and matter functor blindness",
            "current_status": "not_derived",
            "valid_for_claim": "false",
        },
        {
            "step_id": "ABT588_5_theorem_result",
            "mathematical_statement": "If ABT588_1 through ABT588_4 hold, S_X is locally silent: it creates neither a physical X pole, nor Y backreaction, nor edge/test charge.",
            "what_it_buys": "would justify K_X=0, Qbar_edge_XH=0, qbar_XT=0 for this branch",
            "required_input": "all prior theorem clauses together",
            "current_status": "conditional_only",
            "valid_for_claim": "false",
        },
    ]


def make_kill_attempt() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "BKA588_0_use_HZZ_zero",
            "route": "use affine Vdef / H_ZZ=0",
            "test_result": "necessary_but_insufficient",
            "why": "removes a kinetic X pole but leaves (DC)^dagger X in the Y equations",
            "next_needed": "adjoint zero-mode or first-class gauge proof",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "BKA588_1_use_CX_on_shell",
            "route": "set C_X=0 from X equation",
            "test_result": "insufficient",
            "why": "C_X=0 does not imply X=0 and does not remove X delta_Y C_X",
            "next_needed": "solve/kill adjoint equation for X",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "BKA588_2_noether_identity_route",
            "route": "make C_X a Noether identity of S0",
            "test_result": "best_theorem_route",
            "why": "then the multiplier enforces redundancy rather than new physics",
            "next_needed": "construct theta_Y, Omega_Y, v_X, and G[epsilon]",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "BKA588_3_adjoint_coercivity_route",
            "route": "prove ||(DC)^dagger X||^2 >= m_adj^2 ||X||^2 with proper/reference boundary conditions",
            "test_result": "clean_kill_if_proved",
            "why": "the Y equation then forces X=0 on the local branch",
            "next_needed": "explicit DC operator and boundary domain",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "BKA588_4_boundary_counterterm_route",
            "route": "cancel or exactify all boundary pairings",
            "test_result": "required_not_optional",
            "why": "bulk silence still fails if Q_edge survives",
            "next_needed": "B_X exact/pure-gauge/proper-gauge certificate",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "BKA588_5_current_corpus_verdict",
            "route": "promote local no-pole now",
            "test_result": "fail_for_current_claim",
            "why": "DC, adjoint domain, Noether identity, matter quotient, and boundary primitive are not explicit",
            "next_needed": "589 certificate or fallback edge row",
            "valid_for_claim": "false",
        },
    ]


def make_constraint_identity_gate() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CIG588_0_identity",
            "possibility": "C_X=N(E0) Noether/Bianchi identity",
            "local_effect": "no new solution restriction; X is gauge/reference data",
            "claim_requirement": "show N and parent symmetry explicitly",
            "current_status": "not_derived",
        },
        {
            "gate_id": "CIG588_1_first_class_constraint",
            "possibility": "C_X first-class with pi_X primary constraint",
            "local_effect": "removes the X pair from phase space",
            "claim_requirement": "Dirac closure and differentiable generator with zero edge charge",
            "current_status": "not_derived",
        },
        {
            "gate_id": "CIG588_2_second_class_auxiliary",
            "possibility": "C_X is a second-class auxiliary equation",
            "local_effect": "can change Y dynamics or impose hidden source restrictions",
            "claim_requirement": "not acceptable for derived local GR unless residuals are bounded",
            "current_status": "not_excluded",
        },
        {
            "gate_id": "CIG588_3_closure_equation",
            "possibility": "C_X inserted as closure/readout condition",
            "local_effect": "useful modelling branch but not parent derivation",
            "claim_requirement": "demote to edge/q_loc/PPN residual runner",
            "current_status": "fallback_live",
        },
    ]


def make_edge_budget(edge_targets: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target in edge_targets:
        bound = float(target["review_candidate_alpha_bound"])
        equal_three_factor = bound ** (1.0 / 3.0)
        equal_two_factor = math.sqrt(bound)
        rows.append(
            {
                "budget_id": f"EPB588_{len(rows)}",
                "lambda_m": target["lambda_m"],
                "lambda_um": target["lambda_um"],
                "alpha_edge_ceiling": f"{bound:.12g}",
                "if_K_and_qbar_order_one_Qbar_max": f"{bound:.12g}",
                "if_K_order_one_equal_Qbar_qbar_max": f"{equal_two_factor:.12g}",
                "equal_three_factor_max": f"{equal_three_factor:.12g}",
                "largest_tested_prior_that_passes": target["largest_tested_prior_that_passes"],
                "smallest_tested_prior_that_fails": target["smallest_tested_prior_that_fails"],
                "interpretation": "diagnostic_factor_budget_not_source_backed",
                "valid_for_claim": "false",
            }
        )
    return rows


def make_decision(edge_budget: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tightest = min(edge_budget, key=lambda row: float(row["alpha_edge_ceiling"]))
    return [
        {
            "decision_id": "D588_0_adjoint_theorem_written",
            "decision": "the exact multiplier backreaction kill theorem is now stated",
            "meaning": "need C_X as identity/first-class plus no adjoint zero modes plus boundary/matter silence",
            "claim_status": "conditional_not_proved",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D588_1_current_kill_attempt_fails_claim",
            "decision": "current corpus cannot yet force X=0 or prove C_X is pure Noether identity",
            "meaning": "H_ZZ=0 and C_X=0 are not enough to promote no-pole/local-GR",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D588_2_edge_budget_written",
            "decision": "fallback edge-product factor budget written",
            "meaning": f"tightest private target is lambda={tightest['lambda_um']} um with product ceiling {tightest['alpha_edge_ceiling']}",
            "claim_status": "nonclaim_diagnostic",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU588_0_allowed",
            "allowed_after_588": "try to construct the adjoint zero-mode certificate for C_X",
            "forbidden_after_588": "claim multiplier silence from H_ZZ=0 or C_X=0 alone",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU588_1_allowed",
            "allowed_after_588": "use edge-product budgets as fallback diagnostic targets",
            "forbidden_after_588": "turn diagnostic budgets into claim-grade alpha rows",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU588_2_allowed",
            "allowed_after_588": "demote to residual branch if C_X is second-class or closure-only",
            "forbidden_after_588": "hide second-class constraints under gauge/no-pole wording",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary() -> list[dict[str, Any]]:
    return [
        {
            "summary_id": "S588_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "best_private_read": "The route is alive but stricter: affine X must be a first-class/Noether multiplier whose adjoint equation kills X and whose boundary/matter charges vanish.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    kill_rows: list[dict[str, Any]],
    identity_rows: list[dict[str, Any]],
    budget_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    prior_rows = read_csv(PRIOR_587_VALIDATION)
    prior_failures = [row for row in prior_rows if row.get("result", "").strip().lower() != "pass"]
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in theorem_rows if row["valid_for_claim"] == "true"],
        *[row for row in kill_rows if row["valid_for_claim"] == "true"],
        *[row for row in budget_rows if row["valid_for_claim"] == "true"],
    ]
    adjoint_clause = any(row["step_id"] == "ABT588_2_adjoint_zero_mode_kill" for row in theorem_rows)
    current_fail = any(row["attempt_id"] == "BKA588_5_current_corpus_verdict" and "fail" in row["test_result"] for row in kill_rows)
    second_class_retained = any(row["gate_id"] == "CIG588_2_second_class_auxiliary" for row in identity_rows)
    tightest = min(budget_rows, key=lambda row: float(row["alpha_edge_ceiling"]))
    return [
        {
            "check_id": "V588_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V588_1_prior_587_clean",
            "result": "pass" if prior_rows and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V588_2_adjoint_theorem_clause_present",
            "result": "pass" if adjoint_clause else "fail",
            "detail": f"theorem_rows={len(theorem_rows)}",
        },
        {
            "check_id": "V588_3_current_kill_attempt_not_promoted",
            "result": "pass" if current_fail else "fail",
            "detail": "current corpus lacks DC/adjoint-domain/Noether-boundary inputs",
        },
        {
            "check_id": "V588_4_second_class_risk_retained",
            "result": "pass" if second_class_retained else "fail",
            "detail": f"identity_gate_rows={len(identity_rows)}",
        },
        {
            "check_id": "V588_5_edge_budget_complete_nonclaim",
            "result": "pass" if budget_rows and not any(row["valid_for_claim"] == "true" for row in budget_rows) else "fail",
            "detail": f"budget_rows={len(budget_rows)};tightest_lambda_um={tightest['lambda_um']};tightest_ceiling={tightest['alpha_edge_ceiling']}",
        },
        {
            "check_id": "V588_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V588_7_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    kill_rows: list[dict[str, Any]],
    identity_rows: list[dict[str, Any]],
    budget_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 588 Y5 R10 multiplier backreaction kill or bound edge product

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- The exact kill condition is now clear: for `S=S0[Y]+<X,C[Y]>`, the dangerous term is `(DC)^dagger X` in the `Y` equations.
- So the route only works if `C_X` is a Noether/first-class identity and the adjoint equation plus proper/reference boundary conditions force `X=0`.
- Current MTS has not supplied the explicit `DC`, adjoint domain, zero-mode proof, matter quotient, or boundary primitive, so no R10/local-GR promotion is allowed.
- The fallback is now budgeted: if the edge survives, the product `K_edge Qbar_edge_XH qbar_XT` must fit the lambda-by-lambda ceilings, with the tightest private target near `608.0783 um`.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Adjoint Backreaction Theorem
{markdown_table(theorem_rows, ["step_id", "mathematical_statement", "what_it_buys", "required_input", "current_status", "valid_for_claim"])}

## Backreaction Kill Attempt
{markdown_table(kill_rows, ["attempt_id", "route", "test_result", "why", "next_needed", "valid_for_claim"])}

## Constraint Identity Or New Equation Gate
{markdown_table(identity_rows, ["gate_id", "possibility", "local_effect", "claim_requirement", "current_status"])}

## Edge Product Factor Budget
{markdown_table(budget_rows, ["budget_id", "lambda_um", "alpha_edge_ceiling", "if_K_and_qbar_order_one_Qbar_max", "if_K_order_one_equal_Qbar_qbar_max", "equal_three_factor_max", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_rows, ["route_id", "allowed_after_588", "forbidden_after_588", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is a proper engineering answer, not a vibes answer: a multiplier only helps if the adjoint problem has no physical zero mode. If that certificate can be built, the local route gets much stronger. If it cannot, we stop trying to win by theorem and score the surviving edge product honestly.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = RUNS / f"{stamp}-Y5-R10-multiplier-backreaction-kill-or-bound-edge-product"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = source_register()
    edge_targets = read_csv(PRIOR_587_EDGE_TARGETS)
    theorem_rows = make_adjoint_theorem()
    kill_rows = make_kill_attempt()
    identity_rows = make_constraint_identity_gate()
    budget_rows = make_edge_budget(edge_targets)
    decision_rows = make_decision(budget_rows)
    route_rows = make_route_update()
    summary_rows = make_summary()
    validation_rows = make_validation(sources, theorem_rows, kill_rows, identity_rows, budget_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(
        ADJOINT_THEOREM_PATH,
        theorem_rows,
        ["step_id", "mathematical_statement", "what_it_buys", "required_input", "current_status", "valid_for_claim"],
    )
    write_csv(
        KILL_ATTEMPT_PATH,
        kill_rows,
        ["attempt_id", "route", "test_result", "why", "next_needed", "valid_for_claim"],
    )
    write_csv(
        CONSTRAINT_IDENTITY_PATH,
        identity_rows,
        ["gate_id", "possibility", "local_effect", "claim_requirement", "current_status"],
    )
    write_csv(
        EDGE_BUDGET_PATH,
        budget_rows,
        [
            "budget_id",
            "lambda_m",
            "lambda_um",
            "alpha_edge_ceiling",
            "if_K_and_qbar_order_one_Qbar_max",
            "if_K_order_one_equal_Qbar_qbar_max",
            "equal_three_factor_max",
            "largest_tested_prior_that_passes",
            "smallest_tested_prior_that_fails",
            "interpretation",
            "valid_for_claim",
        ],
    )
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_rows, ["route_id", "allowed_after_588", "forbidden_after_588", "next_action"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        ["summary_id", "claim_allowed", "R10_pass", "WEP_pass", "PPN_pass", "local_GR_pass", "best_private_read", "next_target"],
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated,
        run_root,
        sources,
        theorem_rows,
        kill_rows,
        identity_rows,
        budget_rows,
        decision_rows,
        route_rows,
        validation_rows,
    )

    status_payload = {
        "generated": generated,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC_PATH),
        "validation": rel(VALIDATION_PATH),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_root / "COMPLETE.marker").write_text("complete\n", encoding="utf-8")
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
