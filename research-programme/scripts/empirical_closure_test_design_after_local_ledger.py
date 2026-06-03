from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "empirical-closure-test-design-after-local-ledger"
STATUS = "empirical_closure_test_design_written_after_local_ledger_no_scores_generated"
CLAIM_CEILING = "test_design_and_dryrun_commands_only_no_empirical_support_claim"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "280-local-branch-status-ledger-and-empirical-closure-pivot.md", "local branch status ledger and empirical pivot"),
        (ROOT / "runs" / "20260601-000098-local-branch-status-ledger-and-empirical-closure-pivot" / "results" / "status_ledger.csv", "status classes for derived/closure/failed labels"),
        (ROOT / "scripts" / "local_bound_preflight_and_baseline_comparison.py", "local proxy bound preflight runner"),
        (ROOT / "scripts" / "cosmo_SN_BAO_closure_runner.py", "SN+BAO dry-run / short smoke runner"),
        (ROOT / "scripts" / "fixed_vs_kappa_cosmology_runner.py", "fixed 2/27 vs kappa-free cosmology runner"),
        (ROOT / "scripts" / "official_CMB_likelihood_preflight.py", "official CMB asset/interface preflight"),
        (ROOT / "scripts" / "empirical_closure_test_design_after_local_ledger.py", "this empirical design gate"),
    ]
    return [
        {"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"}
        for path, role in sources
    ]


def closure_branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "local_projected_Qcoh_closure",
            "label": "explicit_effective_closure",
            "derived_inputs": "fixed-D Qcoh projection; Ccoh shape derivative",
            "closure_inputs": "physical D; relative representative; projected matter metric",
            "primary_observable": "local residual proxy / PPN-like bound vector",
            "claim_ceiling": "closure_viability_only",
        },
        {
            "branch": "cosmology_no_clock_2over27",
            "label": "empirical_EFT_closure",
            "derived_inputs": "conditional cubic shape from 3D coherent load",
            "closure_inputs": "Bmem=2/27; u3; Hstar=H0; CMB bridge",
            "primary_observable": "SN/BAO background residuals; no-SH0ES branch; fixed-vs-kappa penalty",
            "claim_ceiling": "empirical_closure_score_only",
        },
        {
            "branch": "smooth_Pi_boundary_polarization",
            "label": "closure_only_or_rejected_for_promotion",
            "derived_inputs": "none beyond endpoint constraints",
            "closure_inputs": "Pi(Ccoh) function choice",
            "primary_observable": "domain-sensitivity/local-bound stress only if explicitly parameterized",
            "claim_ceiling": "do_not_use_as_derivation",
        },
        {
            "branch": "topological_representative_selection",
            "label": "future_theorem_target",
            "derived_inputs": "relative current formal closure/admissibility",
            "closure_inputs": "physical representative selection",
            "primary_observable": "not directly testable until theorem exists",
            "claim_ceiling": "derivation_research_only",
        },
    ]


def test_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "T1_local_proxy_bound_preflight",
            "arena": "local_gravity_proxy",
            "runner": "scripts/local_bound_preflight_and_baseline_comparison.py",
            "phase": "dryrun_proxy",
            "models_or_branches": "GR_silence_baseline; MTS_local_projected_Qcoh_closure; leak_stress_cases",
            "required_outputs": "preflight_input.csv; baseline_comparison.csv; gate_results.csv; decision.csv",
            "acceptance_gate": "no support claim; residual proxy must stay below gate or mark failed closure",
            "priority": "high",
        },
        {
            "test_id": "T2_SN_BAO_dryrun_schema",
            "arena": "cosmology_background",
            "runner": "scripts/cosmo_SN_BAO_closure_runner.py",
            "phase": "dry-run",
            "models_or_branches": "LCDM; wCDM; CPL; MTS_fixed_p3_u3quarter; MTS_Bmem_zero; optional p/u3 ablations",
            "required_outputs": "model_matrix.csv; amplitude_policy.csv; baseline_fairness.csv; data_schema_report.csv; status.json",
            "acceptance_gate": "data paths/schema valid before any short-smoke score is read",
            "priority": "high",
        },
        {
            "test_id": "T3_fixed_vs_kappa_SN_BAO_short_smoke",
            "arena": "cosmology_background",
            "runner": "scripts/fixed_vs_kappa_cosmology_runner.py",
            "phase": "dry-run_then_short-smoke",
            "models_or_branches": "LCDM; wCDM; CPL; MTS_fixed_2over27_no_clock; MTS_kappa_free_no_clock; MTS_Bmem_zero",
            "required_outputs": "fit_summary.csv; baseline_comparison.csv; prior_edge_table.csv; residual plots/register",
            "acceptance_gate": "all models converge; edge-hit branches labelled unstable; AIC/BIC compared to LCDM/wCDM/CPL",
            "priority": "high",
        },
        {
            "test_id": "T4_no_SH0ES_branch",
            "arena": "cosmology_background",
            "runner": "scripts/cosmo_SN_BAO_closure_runner.py",
            "phase": "short-smoke",
            "models_or_branches": "same as T2 but SN shape with nuisance offset only",
            "required_outputs": "fit_summary.csv; baseline_comparison.csv; prior_edge_table.csv; residuals",
            "acceptance_gate": "MTS preference cannot depend entirely on local-H0 calibration pressure",
            "priority": "high_after_T2",
        },
        {
            "test_id": "T5_domain_sensitivity_jackknife",
            "arena": "local_and_cosmology_closure_stability",
            "runner": "new_runner_needed",
            "phase": "design_then_short",
            "models_or_branches": "MTS closure variants plus comparable baseline nuisance/split tests",
            "required_outputs": "split_summary.csv; per_split_AIC_BIC.csv; edge_table.csv; failure_labels.csv",
            "acceptance_gate": "MTS not singled out for tests that baselines also fail; instability must be attributed to pipeline if shared",
            "priority": "medium_high",
        },
        {
            "test_id": "T6_official_CMB_preflight_repeat",
            "arena": "CMB",
            "runner": "scripts/official_CMB_likelihood_preflight.py",
            "phase": "asset_preflight_only",
            "models_or_branches": "LCDM baseline; MTS effective background only after official assets exist",
            "required_outputs": "interface_status.csv; asset_manifest.csv; tiny_LCDM_smoke.csv; decision.csv",
            "acceptance_gate": "no CMB support claim without official likelihood assets and reproducible baseline",
            "priority": "medium",
        },
    ]


def baseline_parity_rows() -> list[dict[str, Any]]:
    return [
        {
            "rule": "same_data_same_splits",
            "meaning": "MTS and baselines must see identical rows, covariance treatment, and masks",
            "failure_label": "pipeline_unfair",
        },
        {
            "rule": "same_calibration_freedom_where_comparable",
            "meaning": "if MTS has a nuisance/calibration branch, LCDM/wCDM/CPL get the comparable nuisance treatment",
            "failure_label": "calibration_asymmetry",
        },
        {
            "rule": "same_jackknife_pressure",
            "meaning": "jackknife/split tests are applied to baselines too where the test is meaningful",
            "failure_label": "baseline_not_tested",
        },
        {
            "rule": "complexity_penalty_visible",
            "meaning": "extra MTS freedom and extra baseline freedom are counted in AIC/BIC or explicitly marked not comparable",
            "failure_label": "model_selection_invalid",
        },
        {
            "rule": "edge_hits_not_evidence",
            "meaning": "prior-edge branches can motivate follow-up but cannot be called stable evidence",
            "failure_label": "unstable_evidence",
        },
    ]


def dry_run_command_rows() -> list[dict[str, Any]]:
    py = ".\\.venv-score\\Scripts\\python.exe"
    return [
        {
            "order": 1,
            "name": "local_proxy_bound_preflight",
            "working_directory": str(ROOT),
            "command": f"& '{py}' 'scripts\\local_bound_preflight_and_baseline_comparison.py' --timestamp 20260601-000100",
            "expected_runtime": "seconds",
            "writes_scores": "proxy_only",
            "long_run": "no",
        },
        {
            "order": 2,
            "name": "SN_BAO_schema_dryrun",
            "working_directory": str(ROOT),
            "command": f"& '{py}' 'scripts\\cosmo_SN_BAO_closure_runner.py' --phase dry-run --sn-covariance-mode diagonal --sn-observable mu-sh0es --sn-max-rows 250",
            "expected_runtime": "seconds_to_minutes",
            "writes_scores": "no",
            "long_run": "no",
        },
        {
            "order": 3,
            "name": "fixed_vs_kappa_dryrun",
            "working_directory": str(ROOT),
            "command": f"& '{py}' 'scripts\\fixed_vs_kappa_cosmology_runner.py' --phase dry-run --arena SN-BAO-T7 --timestamp 20260601-000101",
            "expected_runtime": "seconds",
            "writes_scores": "no",
            "long_run": "no",
        },
        {
            "order": 4,
            "name": "fixed_vs_kappa_short_smoke",
            "working_directory": str(ROOT),
            "command": f"& '{py}' 'scripts\\fixed_vs_kappa_cosmology_runner.py' --phase short-smoke --arena SN-BAO-T7 --timestamp 20260601-000102 --max-iter 120",
            "expected_runtime": "minutes",
            "writes_scores": "yes_short_smoke",
            "long_run": "no_if_current_sample",
        },
        {
            "order": 5,
            "name": "official_CMB_asset_preflight",
            "working_directory": str(ROOT),
            "command": f"& '{py}' 'scripts\\official_CMB_likelihood_preflight.py' --timestamp 20260601-000103",
            "expected_runtime": "seconds_to_minutes",
            "writes_scores": "no_official_score",
            "long_run": "no",
        },
    ]


def output_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "artifact": "status.json",
            "required": "yes",
            "reason": "machine-readable status and claim ceiling",
        },
        {
            "artifact": "DONE.txt",
            "required": "yes",
            "reason": "completion marker for no-wait workflow",
        },
        {
            "artifact": "source_register.csv",
            "required": "yes",
            "reason": "every cited path exists",
        },
        {
            "artifact": "gate_results.csv",
            "required": "yes",
            "reason": "pass/warn/fail labels before interpretation",
        },
        {
            "artifact": "baseline_comparison.csv",
            "required": "when_scores_exist",
            "reason": "MTS must be compared to LCDM/wCDM/CPL or local GR baseline",
        },
        {
            "artifact": "prior_edge_table.csv",
            "required": "when_scores_exist",
            "reason": "edge-hit branches are unstable evidence",
        },
        {
            "artifact": "residuals_or_plot_register.csv",
            "required": "when_scores_exist",
            "reason": "scores without residuals are not enough",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "A concrete empirical closure test plan is now defined after the local-branch ledger. "
                "It prioritizes local proxy bound preflight, SN+BAO schema/short-smoke tests, fixed-vs-kappa penalty, no-SH0ES branch, domain-sensitivity jackknife, and official CMB preflight. "
                "No scores are generated by this checkpoint; it only freezes fair baselines, labels, commands, and output contracts."
            ),
            "next_target": "run_T1_T2_T3_dryruns_then_short_smoke_if_schema_passes",
        }
    ]


def write_commands_ps1(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        "$ErrorActionPreference = 'Stop'",
        f"Set-Location -LiteralPath '{ROOT}'",
        "# Dry-run / short-smoke commands generated by checkpoint 281.",
        "# Run one at a time; do not treat dry-run outputs as empirical support.",
        "",
    ]
    for row in rows:
        lines.append(f"# {row['order']}. {row['name']} ({row['expected_runtime']})")
        lines.append(str(row["command"]))
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    command_rows = dry_run_command_rows()
    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "closure_branches.csv": (
            closure_branch_rows(),
            ["branch", "label", "derived_inputs", "closure_inputs", "primary_observable", "claim_ceiling"],
        ),
        "test_manifest.csv": (
            test_manifest_rows(),
            ["test_id", "arena", "runner", "phase", "models_or_branches", "required_outputs", "acceptance_gate", "priority"],
        ),
        "baseline_parity_rules.csv": (baseline_parity_rows(), ["rule", "meaning", "failure_label"]),
        "dry_run_commands.csv": (
            command_rows,
            ["order", "name", "working_directory", "command", "expected_runtime", "writes_scores", "long_run"],
        ),
        "output_contract.csv": (output_contract_rows(), ["artifact", "required", "reason"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    commands_path = results_dir / "run_dryruns.ps1"
    write_commands_ps1(commands_path, command_rows)

    missing_sources = [row for row in source_register_rows() if row["exists"] != "yes"]
    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs) + ["run_dryruns.ps1"],
        "missing_sources": missing_sources,
        "scores_generated": False,
        "empirical_support_claim_allowed": False,
        "dryrun_commands_generated": True,
        "recommended_first_runs": ["T1_local_proxy_bound_preflight", "T2_SN_BAO_dryrun_schema", "T3_fixed_vs_kappa_SN_BAO_short_smoke"],
        "next_target": "run_T1_T2_T3_dryruns_then_short_smoke_if_schema_passes",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Empirical closure test design after local branch ledger.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
