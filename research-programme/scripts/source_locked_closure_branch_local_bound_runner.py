from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "source-locked-closure-branch-local-bound-runner"
STATUS = "closure_branch_local_bound_runner_built_budget_only_no_coefficients_no_pass_claim"
CLAIM_CEILING = "source_locked_closure_runner_only_no_WEP_clock_PPN_fifth_force_EH_or_local_GR_pass"
NEXT_TARGET = "370-common-mode-phiC-coefficient-map.md"


SOURCE_DOCS = [
    {
        "path": "354-official-local-bound-source-lock-or-nohair-proof-deepening.md",
        "role": "source-locked local target scales and quarantine policy",
    },
    {
        "path": "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md",
        "role": "original source-locked residual runner and pressure ranking",
    },
    {
        "path": "368-common-mode-class-metric-clock-PPN-residual-gate.md",
        "role": "class-metric closure residual gate to be converted into runner rows",
    },
    {
        "path": "runs/20260601-215000-common-mode-class-metric-clock-PPN-residual-gate/results/source_locked_targets.csv",
        "role": "machine-readable ready/quarantined source-lock targets",
    },
    {
        "path": "runs/20260601-215000-common-mode-class-metric-clock-PPN-residual-gate/results/residual_gate_matrix.csv",
        "role": "machine-readable class-metric residual gate matrix",
    },
    {
        "path": "366-representative-invariant-matter-action-for-lifted-C.md",
        "role": "conditional representative-invariant matter selector, species universality open",
    },
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "EH exterior operator not derived, residual operator must be retained",
    },
]


READY_ROWS = [
    {
        "residual": "eta_WEP",
        "source_locked_scale": 2.8e-15,
        "closure_branch_terms": [
            "hidden_species_specific_F_A",
            "representative_vertex_leakage",
            "class_metric_species_normalization",
        ],
        "coefficients": ["coeff_WEP_species", "coeff_WEP_rep", "coeff_WEP_norm"],
        "current_status": "hardest_ready_gate_budget_only",
    },
    {
        "residual": "gamma_minus_1",
        "source_locked_scale": 2.3e-5,
        "closure_branch_terms": [
            "coeff_gamma_r_grad",
            "light_matter_metric_mismatch",
            "boundary_marker_anisotropy",
            "residual_EH_operator",
        ],
        "coefficients": ["coeff_gamma", "coeff_light", "coeff_marker", "coeff_EH_gamma"],
        "current_status": "budget_only",
    },
    {
        "residual": "alpha_clock_redshift",
        "source_locked_scale": 3.1e-5,
        "closure_branch_terms": [
            "coeff_clock_Delta_phiC_over_DeltaU",
            "clock_sector_hidden_F_clock",
        ],
        "coefficients": ["coeff_clock", "coeff_clock_species"],
        "current_status": "budget_only",
    },
    {
        "residual": "beta_minus_1",
        "source_locked_scale": 7.8e-5,
        "closure_branch_terms": [
            "coeff_beta1_r_grad",
            "coeff_beta2_r_grad_squared",
            "second_order_residual_EH_operator",
        ],
        "coefficients": ["coeff_beta1", "coeff_beta2", "coeff_EH_beta"],
        "current_status": "budget_only",
    },
]


QUARANTINE_ROWS = [
    {
        "residual": "preferred_frame_alpha1_alpha2",
        "reason": "numeric source locks not ingested in this branch and marker/projector covariance not proved",
        "needed_before_scoring": "source-lock preferred-frame bounds and derive no-marker/no-preferred-frame theorem or coefficients",
    },
    {
        "residual": "xi_preferred_location_anisotropy",
        "reason": "preferred-location/anisotropy sector identified but not numeric locked",
        "needed_before_scoring": "source-lock xi/preferred-location bounds and domain-marker coefficient map",
    },
    {
        "residual": "delta_G_or_fifth_force",
        "reason": "fifth-force/inverse-square bounds and branch coefficients are not source-locked here",
        "needed_before_scoring": "dedicated fifth-force source manifest plus grad(phi_C)/bulk/domain force coefficient map",
    },
]


RUNNER_POLICY = [
    {
        "policy": "ready_rows_are_budgets_not_passes",
        "meaning": "gamma, beta, WEP, and clock have source-locked scales but no derived MTS coefficients",
    },
    {
        "policy": "quarantined_rows_are_retained_not_scored",
        "meaning": "preferred-frame, xi, and fifth-force sectors remain visible but cannot be numerically passed",
    },
    {
        "policy": "closure_labels_visible",
        "meaning": "class metric is tested as labelled closure/theorem target, not as derived local GR",
    },
    {
        "policy": "GR_baseline_explicit",
        "meaning": "GR values are comparison baselines; MTS must earn residual suppression through coefficients or theorems",
    },
    {
        "policy": "missing_coefficient_blocks_pass",
        "meaning": "any residual with coefficient_status=missing is automatically no-pass",
    },
]


BASELINE_COMPARISON_ROWS = [
    {
        "arena": "local_GR_baseline",
        "baseline": "GR has gamma=1, beta=1, no WEP violation, no clock violation",
        "MTS_closure_requirement": "closure residual vector must be theorem-zero or below source-locked budgets",
        "current_readout": "not_passed_coefficients_missing",
    },
    {
        "arena": "universal_matter_baseline",
        "baseline": "single metric/coframe gives species universality by postulate in GR",
        "MTS_closure_requirement": "derive universal F(C_D) and no representative vertices",
        "current_readout": "conditional_representative_invariance_species_universality_open",
    },
    {
        "arena": "operator_baseline",
        "baseline": "Einstein-Hilbert exterior operator supplies standard PPN dynamics",
        "MTS_closure_requirement": "derive EH exterior or retain/bound residual operator",
        "current_readout": "EH_operator_open",
    },
    {
        "arena": "stress_pipeline_baseline",
        "baseline": "run comparable stress tests on GR/LCDM/other relevant baselines when applicable",
        "MTS_closure_requirement": "do not interpret baseline/pipeline failure as MTS-only failure",
        "current_readout": "policy_written_not_executed",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The class-metric closure branch now has a source-locked local-bound runner with four budget rows and three quarantined rows; all local pass claims remain blocked.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "derive or parameterize phi_C local gradients against Newtonian potential and clock/PPN/fifth-force channels",
        "pass_condition": "coeff_clock, coeff_gamma, coeff_beta, and coeff_5 are explicit or marked failed",
    },
    {
        "priority": 2,
        "target": "371-WEP-species-universality-or-active-eta-runner.md",
        "task": "try to prove universal F(C_D) across matter sectors or keep eta_WEP as active hardest gate",
        "pass_condition": "species-specific F_A(C_D) is theorem-forbidden or eta_WEP remains budgeted",
    },
    {
        "priority": 3,
        "target": "372-fifth-force-preferred-frame-source-lock-manifest.md",
        "task": "source-lock quarantined fifth-force/preferred-frame/xi sectors before scoring them",
        "pass_condition": "quarantined rows become ready targets or remain explicitly unscored",
    },
]


def format_float(value: float) -> str:
    return f"{value:.6g}"


def ready_budget_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in READY_ROWS:
        terms = row["closure_branch_terms"]
        coefficients = row["coefficients"]
        target = float(row["source_locked_scale"])
        term_count = len(terms)
        equal_share = target / term_count
        rows.append(
            {
                "residual": row["residual"],
                "source_locked_scale": format_float(target),
                "term_count": term_count,
                "equal_share_ceiling_if_unit_coefficients": format_float(equal_share),
                "closure_branch_terms": ";".join(terms),
                "missing_coefficients": ";".join(coefficients),
                "coefficient_status": "missing",
                "runner_status": row["current_status"],
                "pass_claim_allowed": "no",
            }
        )
    return rows


def pressure_ranking_rows() -> list[dict[str, Any]]:
    rows = sorted(ready_budget_rows(), key=lambda item: float(item["source_locked_scale"]))
    for index, row in enumerate(rows, start=1):
        row["rank"] = index
    return rows


def quarantine_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual": row["residual"],
            "runner_status": "quarantined_unscored",
            "reason": row["reason"],
            "needed_before_scoring": row["needed_before_scoring"],
            "pass_claim_allowed": "no",
        }
        for row in QUARANTINE_ROWS
    ]


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


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "ready_budget_rows_written",
            "status": "pass",
            "evidence": "gamma, beta, WEP, and clock rows have source-locked budgets",
        },
        {
            "gate": "quarantined_rows_retained",
            "status": "pass",
            "evidence": "preferred-frame, xi, and fifth-force rows are retained unscored",
        },
        {
            "gate": "pressure_ranking_written",
            "status": "pass",
            "evidence": "ready rows ranked by source-locked target scale",
        },
        {
            "gate": "missing_coefficients_block_pass",
            "status": "pass",
            "evidence": "all ready rows have coefficient_status=missing and pass_claim_allowed=no",
        },
        {
            "gate": "baseline_comparison_policy_written",
            "status": "pass",
            "evidence": "GR/universal matter/operator/stress-pipeline baselines recorded",
        },
        {
            "gate": "local_bound_pass_claim",
            "status": "fail",
            "evidence": "runner is budget-only; no derived coefficients or source locks for quarantined rows",
        },
        {
            "gate": "local_GR_promotion",
            "status": "fail",
            "evidence": "class selection, EH operator, common-mode gradient, and species universality remain open",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "runner_policy.csv", RUNNER_POLICY)
    write_csv(results_dir / "ready_budget_rows.csv", ready_budget_rows())
    write_csv(results_dir / "quarantine_rows.csv", quarantine_rows())
    write_csv(results_dir / "pressure_ranking.csv", pressure_ranking_rows())
    write_csv(results_dir / "baseline_comparison_rows.csv", BASELINE_COMPARISON_ROWS)
    write_csv(results_dir / "gate_results.csv", gate_rows(source_rows))
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 369 source-locked closure-branch local-bound runner artifacts."
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
