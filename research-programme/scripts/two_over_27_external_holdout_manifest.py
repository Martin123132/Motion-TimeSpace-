#!/usr/bin/env python3
"""Predeclare the B_mem=2/27 branch for external holdout testing."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RUNS_ROOT = POST_CHECKPOINT / "runs"

SOURCES = [
    ("empirical_closure_manifest", POST_CHECKPOINT / "83-empirical-closure-test-manifest.md"),
    ("closure_runner_design", POST_CHECKPOINT / "84-closure-test-runner-design.md"),
    ("two_ninth_robustness", POST_CHECKPOINT / "108-two-ninth-fixed-amplitude-robustness.md"),
    ("endpoint_equation_attempt", POST_CHECKPOINT / "110-endpoint-charge-equation-attempt.md"),
    ("variational_owner_attempt", POST_CHECKPOINT / "111-endpoint-quadratic-variational-owner-attempt.md"),
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, Any]]:
    return [{"source": label, "path": str(path), "exists": path.exists()} for label, path in SOURCES]


def frozen_branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "canonical_R_2over27_locked_amplitude",
            "p": 3,
            "u3": 0.25,
            "DeltaR": 2.0 / 9.0,
            "B_mem": 2.0 / 27.0,
            "eta": 1,
            "a_F": 1,
            "fit_status": "B_mem_frozen_not_fitted",
            "claim_ceiling": "predeclared_empirical_holdout_branch_not_theory_prediction",
        }
    ]


def holdout_rows() -> list[dict[str, Any]]:
    return [
        {
            "holdout": "CMB_distance_prior",
            "data_role": "external_background_distance",
            "amplitude_rule": "B_mem fixed at 2/27 before scoring",
            "baseline_rule": "score LCDM, wCDM, CPL with same nuisance/calibration assumptions",
            "pass_condition": "competitive AIC/BIC without unfreezing B_mem or moving CMB calibration by hand",
            "fail_condition": "requires amplitude/calibration freedom that baselines do not receive",
            "priority": 1,
        },
        {
            "holdout": "growth_fsigma8",
            "data_role": "structure_growth",
            "amplitude_rule": "background B_mem fixed; growth response must be predeclared",
            "baseline_rule": "compare against LCDM/wCDM growth predictions under same data covariance",
            "pass_condition": "does not blow up growth residuals and reports fair baseline failures/successes",
            "fail_condition": "growth sector needs a new fitted suppression knob",
            "priority": 2,
        },
        {
            "holdout": "BAO_only_DR1_DR2_release",
            "data_role": "SN-independent distance stress",
            "amplitude_rule": "B_mem fixed; no SN refit",
            "baseline_rule": "DR1 and DR2 both reported, no cherry-pick",
            "pass_condition": "locked branch remains same-order competitive across releases",
            "fail_condition": "works only for one release or needs BAO-specific amplitude",
            "priority": 3,
        },
        {
            "holdout": "Pantheon_split_rechecks",
            "data_role": "non-holdout robustness only",
            "amplitude_rule": "B_mem fixed, no split retuning",
            "baseline_rule": "same split masks for every model",
            "pass_condition": "confirms no obvious pipeline artifact",
            "fail_condition": "split instability unique to locked branch",
            "priority": 4,
        },
        {
            "holdout": "future_non_SN_cosmology",
            "data_role": "true future/external validation",
            "amplitude_rule": "B_mem=2/27 remains frozen before data ingestion",
            "baseline_rule": "pre-register model count and nuisance handling",
            "pass_condition": "survives without post-hoc amplitude edits",
            "fail_condition": "amplitude must be changed after seeing new data",
            "priority": 5,
        },
    ]


def discipline_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "amplitude_freeze",
            "requirement": "B_mem must equal 2/27 in every holdout score.",
            "failure_label": "amplitude_unfrozen_invalidates_holdout",
        },
        {
            "gate": "same_baseline_data",
            "requirement": "Baselines and MTS use identical rows, covariance, nuisance assumptions, and release labels.",
            "failure_label": "baseline_asymmetry_invalidates_scorecard",
        },
        {
            "gate": "no_theory_promotion",
            "requirement": "Holdout success can upgrade empirical status, not parent-action derivation.",
            "failure_label": "overclaim_invalidates_interpretation",
        },
        {
            "gate": "edge_and_failure_reporting",
            "requirement": "Prior-edge and convergence failures are reported symmetrically for MTS and baselines.",
            "failure_label": "hidden_instability_invalidates_scorecard",
        },
        {
            "gate": "predeclared_growth_response",
            "requirement": "Growth/CMB perturbation response must be fixed before scoring, not tuned after residuals.",
            "failure_label": "growth_rescue_knob_invalidates_holdout",
        },
    ]


def command_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "template": "SN_BAO_locked_branch_extension",
            "command_status": "design_needed",
            "command": ".\\.venv-score\\Scripts\\python.exe scripts\\cosmo_SN_BAO_closure_runner.py --locked-B-mem 0.07407407407407407 ...",
            "note": "runner does not yet expose --locked-B-mem; add only when implementing the next score runner",
        },
        {
            "template": "CMB_growth_locked_branch",
            "command_status": "design_needed",
            "command": ".\\.venv-score\\Scripts\\python.exe scripts\\locked_2over27_CMB_growth_holdout.py --dry-run",
            "note": "new runner must separate background lock from perturbation/growth closure assumptions",
        },
        {
            "template": "BAO_only_release_locked_branch",
            "command_status": "design_needed",
            "command": ".\\.venv-score\\Scripts\\python.exe scripts\\locked_2over27_BAO_only_release_test.py --dry-run",
            "note": "must report DR1 and DR2 together",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision": "verdict", "value": "Bmem_2over27_predeclared_for_external_holdouts"},
        {"decision": "frozen_branch", "value": "canonical_R_2over27_locked_amplitude"},
        {"decision": "locked_B_mem", "value": 2.0 / 27.0},
        {"decision": "locked_DeltaR", "value": 2.0 / 9.0},
        {"decision": "claim_ceiling", "value": "external_holdout_empirical_branch_not_prediction"},
        {"decision": "theory_promotion_allowed", "value": False},
        {"decision": "next_action", "value": "implement_dry_run_locked_2over27_CMB_or_BAO_only_runner"},
    ]


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-two-over-27-external-holdout-manifest"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    missing = [row for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"Missing holdout manifest sources: {missing}")

    frozen_branch = frozen_branch_rows()
    holdouts = holdout_rows()
    gates = discipline_gate_rows()
    commands = command_template_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists"])
    write_csv(results_dir / "frozen_branch_register.csv", frozen_branch, ["branch", "p", "u3", "DeltaR", "B_mem", "eta", "a_F", "fit_status", "claim_ceiling"])
    write_csv(results_dir / "holdout_queue.csv", holdouts, ["holdout", "data_role", "amplitude_rule", "baseline_rule", "pass_condition", "fail_condition", "priority"])
    write_csv(results_dir / "discipline_gates.csv", gates, ["gate", "requirement", "failure_label"])
    write_csv(results_dir / "command_templates.csv", commands, ["template", "command_status", "command", "note"])
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value"])

    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "readout": decisions[0]["value"],
        "locked_B_mem": 2.0 / 27.0,
        "locked_DeltaR": 2.0 / 9.0,
        "holdouts_predeclared": len(holdouts),
        "claim_ceiling": "external_holdout_empirical_branch_not_prediction",
        "theory_promotion_allowed": False,
        "next_action": "implement_dry_run_locked_2over27_CMB_or_BAO_only_runner",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
