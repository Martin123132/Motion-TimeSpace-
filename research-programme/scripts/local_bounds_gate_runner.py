#!/usr/bin/env python3
"""Run pass/fail screening gates for local closure-deviation branches."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SOURCE_15_STATUS = Path("runs/20260530-232024-local-observables-data-map/status.json")
SOURCE_15_GATES = Path(
    "runs/20260530-232024-local-observables-data-map/results/mts_parameter_screening_gates.csv"
)
SOURCE_15_TRANSLATIONS = Path(
    "runs/20260530-232024-local-observables-data-map/results/observable_bound_translations.csv"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def screening_gates(rows: list[dict[str, str]]) -> dict[str, float]:
    return {row["mts_parameter"]: float(row["adopted_screening_gate"]) for row in rows}


def coefficient_map(rows: list[dict[str, str]]) -> dict[str, float]:
    return {
        row["observable"] + "_vs_" + row["mts_parameter"]: float(row["linear_coefficient"])
        for row in rows
    }


def candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "closure_null",
            "q_R": 0.0,
            "delta_beta": 0.0,
            "alpha_clock": 0.0,
            "epsilon_matter": 0.0,
            "reciprocal_charge_QR": 0.0,
            "branch_type": "control_baseline",
            "interpretation": "exact closure; should pass but is not a novel MTS signal",
        },
        {
            "branch": "qR_at_cassini_gate",
            "q_R": 2.3e-5,
            "delta_beta": 0.0,
            "alpha_clock": 0.0,
            "epsilon_matter": 0.0,
            "reciprocal_charge_QR": 0.0,
            "branch_type": "edge_case",
            "interpretation": "gamma-like leakage exactly at adopted Cassini screening gate",
        },
        {
            "branch": "qR_ten_times_gate",
            "q_R": 2.3e-4,
            "delta_beta": 0.0,
            "alpha_clock": 0.0,
            "epsilon_matter": 0.0,
            "reciprocal_charge_QR": 0.0,
            "branch_type": "fail_probe",
            "interpretation": "gamma-like leakage deliberately too large",
        },
        {
            "branch": "beta_at_inpop_gate",
            "q_R": 0.0,
            "delta_beta": 7.16e-5,
            "alpha_clock": 0.0,
            "epsilon_matter": 0.0,
            "reciprocal_charge_QR": 0.0,
            "branch_type": "edge_case",
            "interpretation": "beta drift exactly at adopted INPOP screening gate",
        },
        {
            "branch": "beta_above_gate",
            "q_R": 0.0,
            "delta_beta": 1.0e-4,
            "alpha_clock": 0.0,
            "epsilon_matter": 0.0,
            "reciprocal_charge_QR": 0.0,
            "branch_type": "fail_probe",
            "interpretation": "beta drift beyond adopted screening gate",
        },
        {
            "branch": "clock_at_galileo_gate",
            "q_R": 0.0,
            "delta_beta": 0.0,
            "alpha_clock": 2.48e-5,
            "epsilon_matter": 0.0,
            "reciprocal_charge_QR": 0.0,
            "branch_type": "edge_case",
            "interpretation": "clock/load anomaly at Galileo redshift gate",
        },
        {
            "branch": "matter_above_microscope_gate",
            "q_R": 0.0,
            "delta_beta": 0.0,
            "alpha_clock": 0.0,
            "epsilon_matter": 1.0e-14,
            "reciprocal_charge_QR": 0.0,
            "branch_type": "fail_probe",
            "interpretation": "matter-coupling spread violates MICROSCOPE-derived screening gate",
        },
        {
            "branch": "kinetic_QR_hair_small_gamma",
            "q_R": 1.0e-6,
            "delta_beta": 0.0,
            "alpha_clock": 0.0,
            "epsilon_matter": 0.0,
            "reciprocal_charge_QR": 1.0e-6,
            "branch_type": "theory_fail_probe",
            "interpretation": "small gamma residual but nonzero reciprocal charge violates closure definition",
        },
        {
            "branch": "mixed_inside_simple_gates",
            "q_R": 1.0e-5,
            "delta_beta": 2.0e-5,
            "alpha_clock": 1.0e-5,
            "epsilon_matter": 1.0e-15,
            "reciprocal_charge_QR": 0.0,
            "branch_type": "candidate_probe",
            "interpretation": "small simultaneous leaks inside one-parameter screening gates",
        },
        {
            "branch": "perihelion_degenerate_but_gamma_fail",
            "q_R": 5.0e-5,
            "delta_beta": 1.0e-4,
            "alpha_clock": 0.0,
            "epsilon_matter": 0.0,
            "reciprocal_charge_QR": 0.0,
            "branch_type": "degeneracy_probe",
            "interpretation": "perihelion combination partly cancels but q_R and beta gates still fail separately",
        },
    ]


def gate_result_rows(candidates: list[dict[str, Any]], gates: dict[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        for parameter, gate in gates.items():
            candidate_key = "reciprocal_charge_QR" if parameter == "Q_R" else parameter
            value = float(candidate[candidate_key])
            margin = gate - abs(value)
            if parameter == "Q_R":
                status = "pass" if value == 0.0 else "fail"
                margin = 0.0 if value == 0.0 else -abs(value)
            else:
                status = "pass" if abs(value) <= gate else "fail"
            rows.append(
                {
                    "branch": candidate["branch"],
                    "parameter": parameter,
                    "value": value,
                    "screening_gate": gate,
                    "abs_value_over_gate": "" if gate == 0.0 else abs(value) / gate,
                    "margin_to_gate": margin,
                    "status": status,
                }
            )
    return rows


def observable_impact_rows(candidates: list[dict[str, Any]], coefficients: dict[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in candidates:
        q_r = float(candidate["q_R"])
        delta_beta = float(candidate["delta_beta"])
        alpha_clock = float(candidate["alpha_clock"])
        epsilon_matter = float(candidate["epsilon_matter"])
        rows.extend(
            [
                {
                    "branch": candidate["branch"],
                    "observable": "solar_light_bending",
                    "shift": coefficients["solar_light_bending_vs_q_R"] * q_r,
                    "unit": "arcsec",
                    "depends_on": "q_R",
                },
                {
                    "branch": candidate["branch"],
                    "observable": "solar_shapiro",
                    "shift": coefficients["solar_shapiro_vs_q_R"] * q_r,
                    "unit": "microseconds",
                    "depends_on": "q_R",
                },
                {
                    "branch": candidate["branch"],
                    "observable": "mercury_perihelion_combined",
                    "shift": coefficients["mercury_perihelion_gamma_vs_q_R"] * q_r
                    + coefficients["mercury_perihelion_beta_vs_delta_beta"] * delta_beta,
                    "unit": "arcsec_per_century",
                    "depends_on": "q_R,delta_beta",
                },
                {
                    "branch": candidate["branch"],
                    "observable": "gps_gravitational_redshift",
                    "shift": coefficients["gps_gravitational_redshift_vs_alpha_clock"] * alpha_clock,
                    "unit": "microseconds_per_day",
                    "depends_on": "alpha_clock",
                },
                {
                    "branch": candidate["branch"],
                    "observable": "eotvos_proxy",
                    "shift": coefficients["eotvos_proxy_vs_epsilon_matter"] * epsilon_matter,
                    "unit": "dimensionless",
                    "depends_on": "epsilon_matter",
                },
            ]
        )
    return rows


def branch_summary_rows(
    candidates: list[dict[str, Any]],
    gate_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_branch: dict[str, list[dict[str, Any]]] = {}
    for result in gate_results:
        by_branch.setdefault(result["branch"], []).append(result)
    for candidate in candidates:
        failures = [row["parameter"] for row in by_branch[candidate["branch"]] if row["status"] == "fail"]
        if not failures and candidate["branch"] == "closure_null":
            verdict = "pass_control_not_signal"
        elif not failures:
            verdict = "pass_screening_not_claim"
        else:
            verdict = "fail_screening"
        rows.append(
            {
                "branch": candidate["branch"],
                "branch_type": candidate["branch_type"],
                "verdict": verdict,
                "failed_parameters": ";".join(failures),
                "claim_allowed": "no_empirical_claim",
                "interpretation": candidate["interpretation"],
            }
        )
    return rows


def failure_mode_rows() -> list[dict[str, Any]]:
    return [
        {
            "failure_mode": "gamma_leak",
            "trigger": "abs(q_R) > q_R_gate",
            "meaning": "reciprocal hair or routing drift would be visible in gamma-like channels",
            "response": "reject branch or derive stronger local suppression",
        },
        {
            "failure_mode": "beta_completion_leak",
            "trigger": "abs(delta_beta) > delta_beta_gate",
            "meaning": "local nonlinear completion fails ephemeris screening",
            "response": "repair beta derivation before any local-GR claim",
        },
        {
            "failure_mode": "clock_load_leak",
            "trigger": "abs(alpha_clock) > alpha_clock_gate",
            "meaning": "clock/load law conflicts with redshift screening",
            "response": "revisit T^2=1-L or clock coupling",
        },
        {
            "failure_mode": "matter_coupling_leak",
            "trigger": "abs(epsilon_matter) > epsilon_matter_gate",
            "meaning": "universal coframe coupling fails WEP screening",
            "response": "define matter charges or enforce universal coupling",
        },
        {
            "failure_mode": "reciprocal_charge_hair",
            "trigger": "Q_R != 0",
            "meaning": "closure branch is no longer closure and reintroduces exterior hair",
            "response": "derive Q_R=0 or demote branch",
        },
        {
            "failure_mode": "degeneracy_hiding",
            "trigger": "perihelion combination small while individual gates fail",
            "meaning": "beta/gamma cancellation can hide in one observable",
            "response": "require individual channel gates, not only combined perihelion",
        },
    ]


def audit_gate_rows(source: dict[str, Any], summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pass_count = sum(1 for row in summary if row["verdict"] != "fail_screening")
    fail_count = sum(1 for row in summary if row["verdict"] == "fail_screening")
    return [
        {
            "gate": "source_15_complete",
            "status": "pass" if source.get("readout") == "local_observables_data_map_screening_ready_not_fit" else "fail",
            "detail": str(source.get("readout")),
        },
        {
            "gate": "candidate_branches_screened",
            "status": "pass",
            "detail": f"{len(summary)} candidate branches screened",
        },
        {
            "gate": "pass_fail_outcomes_present",
            "status": "pass" if pass_count > 0 and fail_count > 0 else "fail",
            "detail": f"pass_like={pass_count}, fail={fail_count}",
        },
        {
            "gate": "closure_null_passes",
            "status": "pass"
            if any(row["branch"] == "closure_null" and row["verdict"] == "pass_control_not_signal" for row in summary)
            else "fail",
            "detail": "exact closure should pass only as a control baseline",
        },
        {
            "gate": "nonzero_QR_fails",
            "status": "pass"
            if any(row["branch"] == "kinetic_QR_hair_small_gamma" and "Q_R" in row["failed_parameters"] for row in summary)
            else "fail",
            "detail": "Q_R hair must fail even if q_R is below gamma gate",
        },
        {
            "gate": "empirical_claim_allowed",
            "status": "fail",
            "detail": "published-bound screening is not a raw likelihood fit",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "gate_runner_status",
            "status": "operational_screening_harness",
            "evidence": "candidate branches receive pass/fail results against published-bound gates",
            "next_action": "use this before allowing any local branch into the main workbench",
        },
        {
            "decision": "closure_status",
            "status": "passes_as_control_only",
            "evidence": "closure_null passes all gates but contains no novelty and no parent derivation",
            "next_action": "keep closure as null lane",
        },
        {
            "decision": "next_target",
            "status": "promotion_gate_summary",
            "evidence": "post-checkpoint branch now has derivation gates plus local empirical screening",
            "next_action": "create 17-post-checkpoint-promotion-gate-summary.md",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Local bounds gate runner.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    source = load_json(root / SOURCE_15_STATUS)
    gates = screening_gates(load_csv(root / SOURCE_15_GATES))
    coefficients = coefficient_map(load_csv(root / SOURCE_15_TRANSLATIONS))
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or root / "runs" / f"{timestamp}-local-bounds-gate-runner"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    candidates = candidate_rows()
    gate_results = gate_result_rows(candidates, gates)
    impacts = observable_impact_rows(candidates, coefficients)
    summary = branch_summary_rows(candidates, gate_results)
    failures = failure_mode_rows()
    audit_gates = audit_gate_rows(source, summary)
    decisions = decision_rows()

    write_csv(results_dir / "candidate_local_branches.csv", candidates, list(candidates[0].keys()))
    write_csv(results_dir / "branch_parameter_gate_results.csv", gate_results, list(gate_results[0].keys()))
    write_csv(results_dir / "branch_observable_impacts.csv", impacts, list(impacts[0].keys()))
    write_csv(results_dir / "candidate_branch_summary.csv", summary, list(summary[0].keys()))
    write_csv(results_dir / "local_bounds_failure_modes.csv", failures, list(failures[0].keys()))
    write_csv(results_dir / "local_bounds_gate_runner_gates.csv", audit_gates, list(audit_gates[0].keys()))
    write_csv(results_dir / "local_bounds_gate_runner_decision.csv", decisions, list(decisions[0].keys()))

    passed = [row["branch"] for row in summary if row["verdict"] != "fail_screening"]
    failed = [row["branch"] for row in summary if row["verdict"] == "fail_screening"]
    readout = "local_bounds_gate_runner_operational_screening_not_fit"
    status = {
        "status": "complete_local_bounds_gate_runner",
        "readout": readout,
        "recommendation": "write_post_checkpoint_promotion_gate_summary_next",
        "next_target": "17-post-checkpoint-promotion-gate-summary.md",
        "uses_published_bound_screening": True,
        "uses_raw_likelihoods": False,
        "empirical_claim_allowed": False,
        "screening_gates": gates,
        "passed_branches": passed,
        "failed_branches": failed,
        "outputs": {
            "candidate_local_branches": str(results_dir / "candidate_local_branches.csv"),
            "branch_parameter_gate_results": str(results_dir / "branch_parameter_gate_results.csv"),
            "branch_observable_impacts": str(results_dir / "branch_observable_impacts.csv"),
            "candidate_branch_summary": str(results_dir / "candidate_branch_summary.csv"),
            "local_bounds_failure_modes": str(results_dir / "local_bounds_failure_modes.csv"),
            "local_bounds_gate_runner_gates": str(results_dir / "local_bounds_gate_runner_gates.csv"),
            "local_bounds_gate_runner_decision": str(results_dir / "local_bounds_gate_runner_decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(readout + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
