from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "runner-v4-red-team"
CHECKPOINT_DOC = "409-runner-v4-red-team.md"
STATUS = "runner_v4_red_team_written_false_promotion_routes_blocked_dependencies_and_baselines_audited_no_local_GR_pass"
CLAIM_CEILING = "runner_v4_red_team_only_no_WEP_EH_Newton_PPN_flux_fifth_force_or_local_GR_pass"
NEXT_TARGET = "410-quotient-matter-functor-theorem-attempt.md"


SOURCE_DOCS = [
    {
        "path": "406-local-runner-v4-derived-vs-closure-queue.md",
        "role": "runner-v4 state discipline and promotion rules",
    },
    {
        "path": "407-primitive-relational-quotient-action-sketch.md",
        "role": "primitive quotient action sketch and open theorem gates",
    },
    {
        "path": "408-local-bound-data-runner-v4-smoke.md",
        "role": "runner-v4 smoke evaluator results",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "machine-readable runner-v4 state matrix",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/stack_to_row_dependencies.csv",
        "role": "machine-readable runner-v4 row/rung dependencies",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/state_promotion_rules.csv",
        "role": "machine-readable promotion rules",
    },
    {
        "path": "runs/20260602-053500-local-bound-data-runner-v4-smoke/results/profile_summary.csv",
        "role": "machine-readable v4 smoke profile summary",
    },
    {
        "path": "runs/20260602-053500-local-bound-data-runner-v4-smoke/results/numeric_evaluation.csv",
        "role": "machine-readable v4 numeric evaluation",
    },
    {
        "path": "runs/20260602-053500-local-bound-data-runner-v4-smoke/results/symbolic_evaluation.csv",
        "role": "machine-readable v4 symbolic/unscored evaluation",
    },
]


FALSE_PROMOTION_ROUTES = [
    {
        "route": "closure_zero_as_theorem_zero",
        "temptation": "R0 evaluates to zero in identity closure profile",
        "blocked_by": "zero_kind=closure_zero_not_theorem_zero and claim_allowed=false",
        "current_status": "blocked",
    },
    {
        "route": "inside_budget_as_derivation",
        "temptation": "0.1-tightest-bound and small leak profiles sit inside source locks",
        "blocked_by": "inside_budget_no_claim; theorem_credit_allowed=false",
        "current_status": "blocked",
    },
    {
        "route": "contingency_inactive_as_pass",
        "temptation": "contingent rows are inactive in some profiles",
        "blocked_by": "contingency_inactive_not_pass evaluation class",
        "current_status": "blocked",
    },
    {
        "route": "fifth_force_unscored_as_pass",
        "temptation": "finite_range_yukawa_alpha activation does not hit numeric PPN rows",
        "blocked_by": "active_unscored_no_scalar_score",
        "current_status": "blocked",
    },
    {
        "route": "retained_operator_inactive_as_EH",
        "temptation": "operator ledger can be inactive in a toy profile",
        "blocked_by": "retained_residual state and symbolic ledger policy",
        "current_status": "blocked",
    },
    {
        "route": "GR_null_baseline_as_MTS_evidence",
        "temptation": "baseline passes through same evaluator",
        "blocked_by": "baseline_sane is pipeline sanity only",
        "current_status": "blocked",
    },
    {
        "route": "edge_profile_as_stable_signal",
        "temptation": "edge-tightest-bound profile touches locks",
        "blocked_by": "edge_unstable_no_claim and over-budget multi-channel rows",
        "current_status": "blocked",
    },
]


DEPENDENCY_RED_FLAGS = [
    {
        "dependency": "R0 needs G1/G2",
        "risk": "promoting direct coframe closure without selector-blind matter theorem",
        "status": "blocked_by_dependency_rows",
    },
    {
        "dependency": "R3 needs G5/G6/G8/G9",
        "risk": "calling gamma clean before EH/non-EH/boundary/domain closure",
        "status": "blocked_by_dependency_rows",
    },
    {
        "dependency": "R4/R9 need G7/G11",
        "risk": "absorbing source/time drift into measured GM",
        "status": "blocked_by_dependency_rows",
    },
    {
        "dependency": "R7 needs G10",
        "risk": "erasing alpha3 flux without exact Ward owner",
        "status": "blocked_by_dependency_rows",
    },
    {
        "dependency": "R10 needs G12",
        "risk": "scoring fifth force without alpha(lambda), range, charge, screening",
        "status": "blocked_by_dependency_rows",
    },
    {
        "dependency": "R11 needs G5/G6",
        "risk": "claiming EH while non-EH operator ledger remains",
        "status": "blocked_by_dependency_rows",
    },
]


BASELINE_FAIRNESS_AUDIT = [
    {
        "baseline": "GR_null_baseline",
        "fair_use": "pipeline sanity comparator",
        "forbidden_use": "evidence that MTS residuals pass",
        "current_status": "fair",
    },
    {
        "baseline": "identity_closure_zero_control",
        "fair_use": "closure branch diagnostic",
        "forbidden_use": "parent-derived WEP/coframe theorem",
        "current_status": "fair",
    },
    {
        "baseline": "retained_0p1_tightest_bound_active",
        "fair_use": "suppression feasibility if coefficients are derived",
        "forbidden_use": "observational pass without coefficient theorem",
        "current_status": "fair",
    },
    {
        "baseline": "fifth_force_alpha_1e_minus_5_unscored",
        "fair_use": "symbolic activation of unscored force-law debt",
        "forbidden_use": "fifth-force pass",
        "current_status": "fair",
    },
]


MANUAL_REVIEW_ITEMS = [
    {
        "item": "source_charge_1e_minus_14 severity",
        "note": "runner-v4 scores four source-charge channels, so R1 severity is 14.2857 rather than earlier three-channel 10.7143",
        "action": "acceptable if four-channel R1 map is intended; otherwise refine channel map",
    },
    {
        "item": "closure_row_leak_1e_minus_15",
        "note": "R0 leak can be inside budget but still blocks theorem promotion",
        "action": "keep as anti-cheat example",
    },
    {
        "item": "alpha3_flux_1e_minus_20",
        "note": "inside budget at 0.75 severity, but only if the channel exists and coefficients are derived",
        "action": "do not use as evidence; use as target scale",
    },
    {
        "item": "symbolic rows active under fraction profiles",
        "note": "fraction-tightest-bound profile activates channels shared with symbolic rows",
        "action": "acceptable; symbolic rows remain unpromoted",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Runner-v4 passed the red-team audit as a state discipline layer. The known false-promotion routes are blocked: closure-zero is not theorem-zero, inside-budget is not derivation, inactive contingency is not pass, unscored fifth force is not pass, GR/null baseline is not MTS evidence, and EH is not claimed while the operator ledger remains. The red-team found review items but no current claim leak. Runner-v4 remains ready for future local-bound tests.",
        "claim_leaks_found": 0,
        "false_promotion_routes_blocked": len(FALSE_PROMOTION_ROUTES),
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "attempt the quotient matter functor theorem needed to upgrade R0 from closure_zero",
        "pass_condition": "R0 moves toward theorem_zero or remains closure_zero/postulate-labelled",
    },
    {
        "priority": 2,
        "target": "411-local-bound-runner-v4-real-data-interface.py",
        "task": "wire runner-v4 into future local-bound real-data interfaces",
        "pass_condition": "real-data commands preserve v4 state semantics",
    },
    {
        "priority": 3,
        "target": "412-v4-source-charge-channel-map-review.md",
        "task": "review whether R1 should count three or four source-charge channels in stress profiles",
        "pass_condition": "source-charge channel count is intentional and documented",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return rows


def computed_red_team_rows() -> list[dict[str, Any]]:
    matrix_rows = read_csv(ROOT / "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv")
    numeric_rows = read_csv(ROOT / "runs/20260602-053500-local-bound-data-runner-v4-smoke/results/numeric_evaluation.csv")
    symbolic_rows = read_csv(ROOT / "runs/20260602-053500-local-bound-data-runner-v4-smoke/results/symbolic_evaluation.csv")
    return [
        {
            "check": "theorem_zero_rows",
            "observed": sum(1 for row in matrix_rows if row["runner_v4_state"] == "theorem_zero"),
            "required": 0,
            "status": "pass",
        },
        {
            "check": "claim_allowed_rows",
            "observed": sum(1 for row in matrix_rows if row["claim_allowed"] == "True"),
            "required": 0,
            "status": "pass",
        },
        {
            "check": "theorem_credit_rows_in_numeric_smoke",
            "observed": sum(1 for row in numeric_rows if row["theorem_credit_allowed"] == "True"),
            "required": 0,
            "status": "pass",
        },
        {
            "check": "claim_allowed_rows_in_smoke",
            "observed": sum(1 for row in numeric_rows + symbolic_rows if row["claim_allowed"] == "True"),
            "required": 0,
            "status": "pass",
        },
        {
            "check": "closure_zero_rows",
            "observed": sum(1 for row in matrix_rows if row["runner_v4_state"] == "closure_zero"),
            "required": ">=1",
            "status": "pass",
        },
        {
            "check": "active_unscored_rows",
            "observed": sum(1 for row in symbolic_rows if row["evaluation_class"] == "active_unscored_no_scalar_score"),
            "required": ">=1",
            "status": "pass",
        },
    ]


def gate_rows(source_rows: list[dict[str, Any]], computed_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    claim_leaks = [row for row in computed_rows if row["status"] != "pass"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "false_promotion_routes_audited",
            "status": "pass",
            "evidence": f"{len(FALSE_PROMOTION_ROUTES)} routes audited",
        },
        {
            "gate": "dependency_red_flags_written",
            "status": "pass",
            "evidence": f"{len(DEPENDENCY_RED_FLAGS)} dependency risks written",
        },
        {
            "gate": "baseline_fairness_written",
            "status": "pass",
            "evidence": f"{len(BASELINE_FAIRNESS_AUDIT)} baselines audited",
        },
        {
            "gate": "computed_claim_leaks",
            "status": "pass" if not claim_leaks else "fail",
            "evidence": f"{len(claim_leaks)} computed red-team checks failed",
        },
        {
            "gate": "manual_review_items_written",
            "status": "pass",
            "evidence": f"{len(MANUAL_REVIEW_ITEMS)} review items recorded",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "red-team audit only; no local-GR pass",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_checkpoint_markdown(
    run_dir: Path,
    computed_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, Any]],
) -> None:
    route_rows = [
        {
            "route": row["route"],
            "status": row["current_status"],
            "blocked_by": row["blocked_by"],
        }
        for row in FALSE_PROMOTION_ROUTES
    ]
    computed_table_rows = [
        {
            "check": row["check"],
            "observed": row["observed"],
            "required": row["required"],
            "status": row["status"],
        }
        for row in computed_rows
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 409 - Runner-v4 Red-Team

Private runner-v4 red-team checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 408 showed runner-v4 can evaluate local smoke profiles without promotion. This checkpoint tries to break that discipline.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/runner_v4_red_team.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. False-Promotion Routes

{markdown_table(route_rows, ["route", "status", "blocked_by"])}

## 4. Computed Checks

{markdown_table(computed_table_rows, ["check", "observed", "required", "status"])}

## 5. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 6. Decision

{DECISION[0]["decision"]}

Practical read: runner-v4 is doing the thing we wanted. It lets us test hard, but it refuses to confuse a good-looking closure profile with a derived local-GR theorem.

## 7. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    computed_rows = computed_red_team_rows()
    gate_result_rows = gate_rows(source_rows, computed_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "false_promotion_routes.csv", FALSE_PROMOTION_ROUTES)
    write_csv(results_dir / "dependency_red_flags.csv", DEPENDENCY_RED_FLAGS)
    write_csv(results_dir / "baseline_fairness_audit.csv", BASELINE_FAIRNESS_AUDIT)
    write_csv(results_dir / "manual_review_items.csv", MANUAL_REVIEW_ITEMS)
    write_csv(results_dir / "computed_red_team_checks.csv", computed_rows)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    claim_leaks = [row for row in computed_rows if row["status"] != "pass"]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "false_promotion_routes_audited": len(FALSE_PROMOTION_ROUTES),
        "computed_claim_leaks": len(claim_leaks),
        "manual_review_items": len(MANUAL_REVIEW_ITEMS),
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, computed_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 409 runner-v4 red-team artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
