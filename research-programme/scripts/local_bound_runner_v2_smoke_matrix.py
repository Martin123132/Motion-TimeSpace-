from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-bound-runner-v2-smoke-matrix"
STATUS = "local_bound_runner_v2_smoke_matrix_written_GR_null_baseline_sane_retained_pullback_rows_budgeted_no_local_GR_pass"
CLAIM_CEILING = "local_bound_smoke_matrix_only_no_WEP_PPN_preferred_frame_fifth_force_EH_or_local_GR_pass"
NEXT_TARGET = "387-identity-coframe-or-class-metric-fork.md"


SOURCE_DOCS = [
    {
        "path": "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md",
        "role": "source-locked PPN and WEP local pressure rows",
    },
    {
        "path": "369-source-locked-closure-branch-local-bound-runner.md",
        "role": "closure branch budget policy and source locks",
    },
    {
        "path": "374-fifth-force-preferred-frame-source-lock-manifest.md",
        "role": "preferred-frame, xi, alpha3, Gdot, and fifth-force guardrails",
    },
    {
        "path": "377-fifth-force-range-coupling-map.md",
        "role": "range/coupling fifth-force contract",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "source-normalization and measured-GM absorption limits",
    },
    {
        "path": "381-local-GR-debt-ledger-rollup-after-360-380.md",
        "role": "local-GR debt rollup before runner v2",
    },
    {
        "path": "383-local-bound-runner-v2-from-retained-residuals.md",
        "role": "runner v2 residual rows and baseline policy",
    },
    {
        "path": "384-parent-action-first-variation-obstruction-map.md",
        "role": "first unowned parent variation term Pi_I^matter",
    },
    {
        "path": "385-observed-coframe-selector-pullback-cancellation-theorem.md",
        "role": "pullback cancellation routes and retained active rows",
    },
    {
        "path": "runs/20260602-011500-local-bound-runner-v2-from-retained-residuals/results/retained_residual_runner_matrix.csv",
        "role": "machine-readable retained residual rows from runner v2",
    },
    {
        "path": "runs/20260602-013500-observed-coframe-selector-pullback-cancellation-theorem/results/pullback_classification.csv",
        "role": "machine-readable pullback classification from checkpoint 385",
    },
]


LOCAL_NUMERIC_ROWS = [
    {
        "row_id": "R1",
        "observable": "eta_WEP",
        "state": "budget_only",
        "source_lock": 2.8e-15,
        "units": "dimensionless",
        "baseline_value": "0",
        "active_pullback_family": "species C_D response; species mass/constant response; test charge split",
        "why_it_matters": "hardest always-relevant local row unless one coframe/common F is derived",
    },
    {
        "row_id": "R2",
        "observable": "alpha_clock_redshift",
        "state": "budget_only",
        "source_lock": 3.1e-5,
        "units": "dimensionless",
        "baseline_value": "0",
        "active_pullback_family": "common class metric; clock-sector constants; coframe mismatch",
        "why_it_matters": "common-mode pullback can be clock-visible even when WEP species split is absent",
    },
    {
        "row_id": "R3",
        "observable": "gamma_minus_1",
        "state": "budget_only",
        "source_lock": 2.3e-5,
        "units": "dimensionless",
        "baseline_value": "0",
        "active_pullback_family": "boundary shear; bulk X; scalar/common mode; higher operator coefficients",
        "why_it_matters": "classic light/curvature PPN row",
    },
    {
        "row_id": "R4",
        "observable": "beta_minus_1",
        "state": "budget_only",
        "source_lock": 7.8e-5,
        "units": "dimensionless",
        "baseline_value": "0",
        "active_pullback_family": "nonlinear boundary/source terms; radial hair; bulk X; higher operators",
        "why_it_matters": "classic nonlinear/radial PPN row",
    },
    {
        "row_id": "R5",
        "observable": "alpha1",
        "state": "budget_only",
        "source_lock": 1.0e-4,
        "units": "dimensionless",
        "baseline_value": "0",
        "active_pullback_family": "domain vector; boundary B_0i; coframe slip",
        "why_it_matters": "preferred-frame row",
    },
    {
        "row_id": "R6",
        "observable": "alpha2",
        "state": "budget_only",
        "source_lock": 2.0e-9,
        "units": "dimensionless",
        "baseline_value": "0",
        "active_pullback_family": "anisotropic coframe; domain vector; marker normal",
        "why_it_matters": "hard preferred-frame/anisotropy row",
    },
    {
        "row_id": "R7",
        "observable": "alpha3",
        "state": "contingent_budget",
        "source_lock": 4.0e-20,
        "units": "dimensionless",
        "baseline_value": "0",
        "active_pullback_family": "unowned boundary flux; momentum nonconservation; Ward-force leakage",
        "why_it_matters": "brutal but contingent; only counts if channel is derived",
    },
    {
        "row_id": "R8",
        "observable": "xi",
        "state": "budget_only",
        "source_lock": 4.0e-9,
        "units": "dimensionless",
        "baseline_value": "0",
        "active_pullback_family": "trace-free boundary shear; domain/external anisotropy; projector leakage",
        "why_it_matters": "preferred-location/anisotropy row",
    },
    {
        "row_id": "R9",
        "observable": "Gdot_over_G",
        "state": "contingent_budget",
        "source_lock": 9.6e-15,
        "units": "yr^-1",
        "baseline_value": "0",
        "active_pullback_family": "time-dependent source normalization; memory drift; boundary flux",
        "why_it_matters": "contingent time-drift guardrail",
    },
]


UNSCORED_ROWS = [
    {
        "row_id": "R10",
        "observable": "delta_G_or_fifth_force_yukawa",
        "state": "unscored_parameterized",
        "required_inputs": "range lambda, coupling alpha(lambda), source charge, screening/composition profile",
        "baseline_value": "no fifth-force beyond measured GM",
        "smoke_policy": "not scalar-scored; keep force-law contract",
    }
]


SMOKE_SCENARIOS = [
    {
        "scenario": "GR_null_baseline",
        "mode": "absolute",
        "value": 0.0,
        "branch": "baseline",
        "interpretation": "GR/null row through the same evaluator; should be inside every local source lock",
        "claim_policy": "baseline sanity only",
    },
    {
        "scenario": "conditional_derived_zero_control",
        "mode": "absolute",
        "value": 0.0,
        "branch": "conditional_zero",
        "interpretation": "what a real theorem-zero would score like if parent-derived",
        "claim_policy": "not available until theorem source is supplied",
    },
    {
        "scenario": "one_tenth_budget_control",
        "mode": "fraction_of_limit",
        "value": 0.1,
        "branch": "budget_control",
        "interpretation": "toy retained coefficient safely below source lock",
        "claim_policy": "inside budget is not a derivation",
    },
    {
        "scenario": "edge_budget_control",
        "mode": "fraction_of_limit",
        "value": 1.0,
        "branch": "budget_edge",
        "interpretation": "toy retained coefficient exactly at source lock",
        "claim_policy": "edge is not stable evidence",
    },
    {
        "scenario": "ten_times_over_budget_control",
        "mode": "fraction_of_limit",
        "value": 10.0,
        "branch": "over_budget",
        "interpretation": "toy retained coefficient ten times too large",
        "claim_policy": "explicit smoke failure",
    },
    {
        "scenario": "floor_leak_1e_minus_12",
        "mode": "absolute",
        "value": 1.0e-12,
        "branch": "absolute_leak_floor",
        "interpretation": "tiny-looking absolute leak; exposes which rows are genuinely brutal",
        "claim_policy": "diagnostic only",
    },
    {
        "scenario": "unit_coupling_stress",
        "mode": "absolute",
        "value": 1.0,
        "branch": "unit_response",
        "interpretation": "raw order-one retained coupling stress",
        "claim_policy": "must fail; used to show required suppression factors",
    },
]


PULLBACK_JOIN = [
    {
        "pullback_piece": "representative_Cperp",
        "runner_rows": "clock/gamma if representative leakage survives",
        "smoke_status": "conditional_gauge_zero_or_budget",
        "next_theory_need": "prove exact quotient-gauge selector",
    },
    {
        "pullback_piece": "physical_class_C_D_common",
        "runner_rows": "alpha_clock_redshift; gamma_minus_1; fifth_force; Gdot_over_G",
        "smoke_status": "common_mode_budget_or_unscored",
        "next_theory_need": "local silence or source-normalized constant mode",
    },
    {
        "pullback_piece": "physical_class_C_D_species",
        "runner_rows": "eta_WEP; composition_fifth_force",
        "smoke_status": "hardest_active_budget",
        "next_theory_need": "identity coframe or parent species symmetry/common F",
    },
    {
        "pullback_piece": "projector_or_domain_selector",
        "runner_rows": "alpha1; alpha2; xi; gamma_minus_1",
        "smoke_status": "preferred_frame_budget",
        "next_theory_need": "covariant projector/domain selector with owned stress",
    },
    {
        "pullback_piece": "boundary_selector",
        "runner_rows": "gamma_minus_1; beta_minus_1; alpha_i; xi; WEP_boundary",
        "smoke_status": "boundary_budget",
        "next_theory_need": "class-only boundary action or Ward-owned harmless flux",
    },
    {
        "pullback_piece": "bulk_X_selector_or_charge",
        "runner_rows": "fifth_force; gamma_minus_1; beta_minus_1; eta_WEP_if_charged",
        "smoke_status": "unscored_or_budget",
        "next_theory_need": "bulk-X no-hair/mass-gap or source-normalized force law",
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


def scenario_value(row: dict[str, Any], scenario: dict[str, Any]) -> float:
    if scenario["mode"] == "fraction_of_limit":
        return float(row["source_lock"]) * float(scenario["value"])
    return float(scenario["value"])


def classify_smoke(row: dict[str, Any], scenario: dict[str, Any], severity: float) -> str:
    if scenario["scenario"] == "GR_null_baseline":
        return "baseline_sane" if severity == 0.0 else "baseline_broken"
    if scenario["scenario"] == "conditional_derived_zero_control":
        return "theorem_zero_would_be_safe_but_not_available" if severity == 0.0 else "control_broken"
    if row["state"] == "contingent_budget" and severity > 1.0:
        return "over_budget_if_channel_exists"
    if severity == 0.0:
        return "inside_budget_zero"
    if severity < 1.0:
        return "inside_budget_smoke_only"
    if severity == 1.0:
        return "on_budget_edge_unstable"
    return "over_budget"


def smoke_matrix_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for local_row in LOCAL_NUMERIC_ROWS:
        for scenario in SMOKE_SCENARIOS:
            residual_value = scenario_value(local_row, scenario)
            source_lock = float(local_row["source_lock"])
            severity = abs(residual_value) / source_lock if source_lock else float("inf")
            rows.append(
                {
                    "row_id": local_row["row_id"],
                    "observable": local_row["observable"],
                    "state": local_row["state"],
                    "source_lock": source_lock,
                    "units": local_row["units"],
                    "scenario": scenario["scenario"],
                    "branch": scenario["branch"],
                    "residual_value": residual_value,
                    "severity_ratio": severity,
                    "smoke_class": classify_smoke(local_row, scenario, severity),
                    "claim_allowed": False,
                    "notes": scenario["interpretation"],
                }
            )
    return rows


def baseline_sanity_rows(matrix_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in matrix_rows:
        if row["scenario"] == "GR_null_baseline":
            rows.append(
                {
                    "observable": row["observable"],
                    "baseline_value": row["residual_value"],
                    "source_lock": row["source_lock"],
                    "severity_ratio": row["severity_ratio"],
                    "baseline_sane": row["smoke_class"] == "baseline_sane",
                    "same_pipeline": True,
                }
            )
    return rows


def suppression_budget_rows(matrix_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unit_rows = [row for row in matrix_rows if row["scenario"] == "unit_coupling_stress"]
    rows: list[dict[str, Any]] = []
    for row in unit_rows:
        rows.append(
            {
                "observable": row["observable"],
                "state": row["state"],
                "source_lock": row["source_lock"],
                "units": row["units"],
                "unit_coupling_severity": row["severity_ratio"],
                "required_abs_coefficient_for_unit_response": row["source_lock"],
                "equal_share_two_terms": row["source_lock"] / 2.0,
                "equal_share_four_terms": row["source_lock"] / 4.0,
                "smoke_priority": "hardest_ready" if row["observable"] == "eta_WEP" else "contingent_brutal" if row["state"] == "contingent_budget" else "budget_row",
            }
        )
    rows.sort(key=lambda item: (item["state"] != "budget_only", item["source_lock"]))
    return rows


def verdict_rows(matrix_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for scenario in SMOKE_SCENARIOS:
        scenario_rows = [row for row in matrix_rows if row["scenario"] == scenario["scenario"]]
        over_budget = [row for row in scenario_rows if row["severity_ratio"] > 1.0]
        edge = [row for row in scenario_rows if row["severity_ratio"] == 1.0]
        inside = [row for row in scenario_rows if row["severity_ratio"] < 1.0]
        rows.append(
            {
                "scenario": scenario["scenario"],
                "branch": scenario["branch"],
                "inside_rows": len(inside),
                "edge_rows": len(edge),
                "over_budget_rows": len(over_budget),
                "claim_allowed": False,
                "verdict": "baseline_sane" if scenario["scenario"] == "GR_null_baseline" and not over_budget else "diagnostic_only_no_pass",
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]], matrix_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    baseline_rows = [row for row in matrix_rows if row["scenario"] == "GR_null_baseline"]
    baseline_sane = all(row["smoke_class"] == "baseline_sane" for row in baseline_rows)
    eta_unit = [
        row for row in matrix_rows
        if row["scenario"] == "unit_coupling_stress" and row["observable"] == "eta_WEP"
    ][0]
    unit_over = [
        row for row in matrix_rows
        if row["scenario"] == "unit_coupling_stress" and row["severity_ratio"] > 1.0
    ]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "numeric_local_rows_loaded",
            "status": "pass",
            "evidence": f"{len(LOCAL_NUMERIC_ROWS)} numeric rows loaded plus {len(UNSCORED_ROWS)} unscored force-law row",
        },
        {
            "gate": "GR_null_baseline_same_pipeline",
            "status": "pass" if baseline_sane else "fail",
            "evidence": f"{len(baseline_rows)} baseline rows evaluated with zero residual",
        },
        {
            "gate": "smoke_scenarios_written",
            "status": "pass",
            "evidence": f"{len(SMOKE_SCENARIOS)} scenarios x {len(LOCAL_NUMERIC_ROWS)} numeric rows = {len(matrix_rows)} smoke rows",
        },
        {
            "gate": "unit_coupling_not_mistaken_for_pass",
            "status": "pass" if len(unit_over) == len(LOCAL_NUMERIC_ROWS) else "fail",
            "evidence": f"{len(unit_over)} of {len(LOCAL_NUMERIC_ROWS)} unit-coupling rows are over budget",
        },
        {
            "gate": "eta_WEP_pressure_visible",
            "status": "pass",
            "evidence": f"unit eta severity ratio = {eta_unit['severity_ratio']}",
        },
        {
            "gate": "fifth_force_kept_unscored",
            "status": "pass",
            "evidence": "delta_G_or_fifth_force_yukawa remains range/coupling/source-charge based",
        },
        {
            "gate": "WEP_PPN_or_local_GR_promoted",
            "status": "fail",
            "evidence": "smoke matrix has no derived coefficients and no parent cancellation of Pi_I^matter",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(matrix_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    unit_rows = [row for row in matrix_rows if row["scenario"] == "unit_coupling_stress"]
    hardest_ready = min(
        (row for row in LOCAL_NUMERIC_ROWS if row["state"] == "budget_only"),
        key=lambda row: row["source_lock"],
    )
    worst_unit = max(unit_rows, key=lambda row: row["severity_ratio"])
    return [
        {
            "status": STATUS,
            "decision": "The GR/null baseline is sane in the same evaluator. Retained pullback rows become budgets, not passes. Order-one retained couplings fail every numeric row; even tiny absolute leaks stress eta_WEP and preferred-frame/contingent rows. The next theory fork must either make the local matter coframe an identity/metric coframe or retain the class-metric pullback as explicit closure/counterstress.",
            "hardest_ready_row": hardest_ready["observable"],
            "hardest_ready_source_lock": hardest_ready["source_lock"],
            "worst_unit_coupling_row": worst_unit["observable"],
            "worst_unit_coupling_severity": worst_unit["severity_ratio"],
            "claim_ceiling": CLAIM_CEILING,
            "next_target": NEXT_TARGET,
        }
    ]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "fork the local theory into strict identity coframe versus retained class-metric pullback, then decide which branch can honestly target local GR",
        "pass_condition": "one branch gets a parent action theorem route or the pullback branch is explicitly demoted to closure/counterstress",
    },
    {
        "priority": 2,
        "target": "388-WEP-species-symmetry-common-F-parent-selector-attempt.md",
        "task": "attempt a parent species symmetry/common-F selector for the hardest eta_WEP row",
        "pass_condition": "F_A(C_D)=F(C_D) is parent-derived or eta_WEP remains active",
    },
    {
        "priority": 3,
        "target": "389-common-mode-source-normalization-local-silence-contract.md",
        "task": "try to turn common C_D pullback into constant source/GM normalization rather than clock/gamma/fifth-force residual",
        "pass_condition": "common mode is theorem-zero, source-normalized, or retained as budget",
    },
]


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    matrix_rows = smoke_matrix_rows()

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "local_numeric_rows.csv", LOCAL_NUMERIC_ROWS)
    write_csv(results_dir / "unscored_rows.csv", UNSCORED_ROWS)
    write_csv(results_dir / "smoke_scenarios.csv", SMOKE_SCENARIOS)
    write_csv(results_dir / "baseline_sanity_matrix.csv", baseline_sanity_rows(matrix_rows))
    write_csv(results_dir / "residual_smoke_matrix.csv", matrix_rows)
    write_csv(results_dir / "suppression_budget_summary.csv", suppression_budget_rows(matrix_rows))
    write_csv(results_dir / "pullback_row_join.csv", PULLBACK_JOIN)
    write_csv(results_dir / "verdict_table.csv", verdict_rows(matrix_rows))
    write_csv(results_dir / "gate_results.csv", gate_rows(source_rows, matrix_rows))
    write_csv(results_dir / "decision.csv", decision_rows(matrix_rows))
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "numeric_local_rows": len(LOCAL_NUMERIC_ROWS),
        "unscored_rows": len(UNSCORED_ROWS),
        "smoke_scenarios": len(SMOKE_SCENARIOS),
        "smoke_matrix_rows": len(matrix_rows),
        "GR_null_baseline_sane": all(row["baseline_sane"] for row in baseline_sanity_rows(matrix_rows)),
        "pass_claim_allowed": False,
        "derived_local_GR_claim_allowed": False,
        "hardest_ready_row": "eta_WEP",
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 386 local-bound runner v2 smoke matrix artifacts."
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
