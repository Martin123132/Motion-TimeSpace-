#!/usr/bin/env python3
"""Create the empirical closure test manifest after amplitude classification."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "40_fresh_holdout_or_official_likelihood_roadmap": Path("40-fresh-holdout-or-official-likelihood-roadmap.md"),
    "43_official_CMB_perturbation_contract": Path("43-official-CMB-perturbation-contract.md"),
    "49_C2_regularized_closure_ledger": Path("49-C2-regularized-closure-ledger.md"),
    "55_u3_quarter_lock_smoke": Path("55-u3-quarter-lock-smoke.md"),
    "80_stress_free_reference_gate": Path("80-stress-free-reference-action-gate.md"),
    "81_post_local_route_pivot_decision": Path("81-post-local-route-pivot-decision.md"),
    "82_amplitude_normalization_gate": Path("82-amplitude-normalization-gate.md"),
    "82_amplitude_register": Path("runs/20260531-121227-amplitude-normalization-gate/results/amplitude_register.csv"),
    "82_empirical_handling": Path("runs/20260531-121227-amplitude-normalization-gate/results/empirical_handling.csv"),
}


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, relative_path in SOURCE_PATHS.items():
        absolute_path = POST_CHECKPOINT / relative_path
        rows.append(
            {
                "source_key": key,
                "relative_path": str(relative_path),
                "absolute_path": str(absolute_path),
                "exists": absolute_path.exists(),
            }
        )
    missing = [row["absolute_path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def test_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "cosmo_background_SN_BAO",
            "arena": "cosmology_background",
            "data_or_proxy": "PantheonPlus_shape_or_SN_with_offset; DESI/BAO distances where available locally",
            "mts_variant": "C2_p3_u3quarter_with_Bmem_fit",
            "fixed_factors": "p=3; u3=1/4",
            "fitted_factors": "B_mem_or_b_mem; standard nuisance/calibration parameters",
            "ablations": "fitted_p; fitted_u3; no_memory; prior_width_sweeps",
            "baselines": "LambdaCDM; wCDM; CPL",
            "required_diagnostics": "chi2; AIC; BIC; residuals; prior_edges; split_stability",
            "claim_ceiling": "closure_performance_only",
        },
        {
            "test_id": "cosmo_growth_CMB_distance_proxy",
            "arena": "cosmology_growth_distance",
            "data_or_proxy": "growth_fsigma8_proxy; CMB_distance_prior_proxy_or_official_likelihood_when_available",
            "mts_variant": "regularized_memory_closure_with_amplitude_priors",
            "fixed_factors": "p=3; u3=1/4",
            "fitted_factors": "B_mem_or_b_mem; Omega_m0/H0_or_calibration_branch_parameters",
            "ablations": "CMB_calibration_free; no_SH0ES; fitted_activation_shape",
            "baselines": "LambdaCDM; wCDM; CPL; same calibration freedom where comparable",
            "required_diagnostics": "distance_residuals; growth_residuals; AIC/BIC; prior_edges; calibration_sensitivity",
            "claim_ceiling": "closure_stress_test_only",
        },
        {
            "test_id": "galaxy_rotation_reference",
            "arena": "galaxy_dynamics",
            "data_or_proxy": "SPARC_or_existing_galaxy_work_outputs",
            "mts_variant": "do_not_import_Ccoh_parent_claim; use explicitly labelled galaxy closure only",
            "fixed_factors": "none_from_cosmo_unless_predeclared",
            "fitted_factors": "galaxy-specific nuisance/mass-to-light where the baseline also gets them",
            "ablations": "fixed_cosmo_amplitude_transfer; fitted_galaxy_amplitude; leave-one-galaxy-out",
            "baselines": "Newtonian_baryonic; standard_empirical_baseline_used_in_repo; MOND-style baseline if implemented fairly",
            "required_diagnostics": "residuals; per-galaxy_chi2; jackknife_against_baselines; parameter_stability",
            "claim_ceiling": "empirical_pillar_not_unified_field_proof",
        },
        {
            "test_id": "local_PPN_residual_bound",
            "arena": "local_gravity",
            "data_or_proxy": "PPN/solar_system/local residual bounds as constraints",
            "mts_variant": "A_loc_or_q_loc_bound_only",
            "fixed_factors": "none_promoted",
            "fitted_factors": "none_as_derived_mechanism",
            "ablations": "turn_local_closure_on_off; bound_A_loc_to_zero",
            "baselines": "GR_PPN",
            "required_diagnostics": "upper_bound_on_residual; preferred_frame_flags; fifth_force_flags",
            "claim_ceiling": "constraint_only",
        },
        {
            "test_id": "EM_time_extension_preflight",
            "arena": "EM_time_extension",
            "data_or_proxy": "fine_structure_clock_or_time_claims_only_after_variable_audit",
            "mts_variant": "no_unified_claim_until_equations_and_units_registered",
            "fixed_factors": "none",
            "fitted_factors": "none_before_manifest",
            "ablations": "dimensional_consistency_first",
            "baselines": "Maxwell/SR/standard_clock_physics",
            "required_diagnostics": "units; covariance; conservation; observable_link",
            "claim_ceiling": "preflight_only",
        },
    ]


def amplitude_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "factor": "p=3",
            "default_policy": "fixed_primary",
            "required_ablation": "fitted_p",
            "failure_flag": "fixed_p_materially_worse_without_theory_gain",
        },
        {
            "factor": "u3=1/4",
            "default_policy": "fixed_primary",
            "required_ablation": "fitted_u3_and_inherited_C2_u3",
            "failure_flag": "quarter_lock_breaks_under_splits_or_refit_comparison",
        },
        {
            "factor": "B_mem/b_mem",
            "default_policy": "fitted_with_explicit_priors",
            "required_ablation": "wide_prior; narrow_prior; Bmem_zero; split_fits",
            "failure_flag": "best_fit_on_prior_edge_or_split_unstable",
        },
        {
            "factor": "Ccoh",
            "default_policy": "diagnostic_only",
            "required_ablation": "Ccoh_off_or_nonselector_closure",
            "failure_flag": "result_depends_on_hidden_selector_claim",
        },
        {
            "factor": "A_loc/q_loc",
            "default_policy": "bound_only",
            "required_ablation": "set_to_zero_GR_limit",
            "failure_flag": "needs_nonzero_local_residual_to_fit_anything",
        },
    ]


def baseline_fairness_rows() -> list[dict[str, Any]]:
    return [
        {
            "baseline_rule": "same_data_splits",
            "requirement": "MTS and baselines use identical train/holdout/jackknife splits",
            "why": "otherwise robustness failures may be pipeline artifacts",
        },
        {
            "baseline_rule": "same_nuisance_freedom_where_applicable",
            "requirement": "do not freeze baseline nuisance parameters while allowing MTS nuisance freedom, or vice versa",
            "why": "prevents false AIC/BIC and residual comparisons",
        },
        {
            "baseline_rule": "same_calibration_branch",
            "requirement": "if MTS gets no-SH0ES or calibration-free branch, baselines get comparable branches",
            "why": "local-H0 pressure cannot be assigned unfairly",
        },
        {
            "baseline_rule": "report_failures_symmetrically",
            "requirement": "if a jackknife breaks MTS and also breaks the baseline, flag pipeline/data sensitivity",
            "why": "a test is not decisive if all comparable models fail it",
        },
        {
            "baseline_rule": "no_claim_from_edge_hits",
            "requirement": "any model whose best fit sits on prior edges is marked unstable",
            "why": "edge-hitting improvement is not stable evidence",
        },
    ]


def output_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "artifact": "fit_summary.csv",
            "required_columns": "model; arena; chi2; dof; AIC; BIC; convergence; prior_edge_flag; claim_ceiling",
            "required_for": "all quantitative fits",
        },
        {
            "artifact": "amplitude_policy.csv",
            "required_columns": "factor; fixed_or_fitted_or_ablated; prior; best_fit; split_variation; status",
            "required_for": "all tests involving p/u3/Bmem/Ccoh/A_loc",
        },
        {
            "artifact": "baseline_comparison.csv",
            "required_columns": "baseline; same_data; same_nuisance; same_calibration; delta_chi2; delta_AIC; delta_BIC",
            "required_for": "all tests with external comparison",
        },
        {
            "artifact": "residuals.csv",
            "required_columns": "dataset; observable; z_or_radius_or_x; observed; predicted; residual; model",
            "required_for": "all data-residual tests",
        },
        {
            "artifact": "status.json",
            "required_columns": "readout; stable_evidence_allowed; failures; next_action",
            "required_for": "every run directory",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "empirical_manifest_status",
            "status": "test_contract_ready_not_yet_executed",
            "evidence": "test arenas, amplitude policies, baseline fairness rules, and output artifacts are specified",
            "next_action": "create 84-closure-test-runner-design.md or implement first short smoke runner",
        },
        {
            "decision": "primary_next_test",
            "status": "cosmo_background_SN_BAO_short_smoke",
            "evidence": "cosmology closure has the clearest amplitude policy and existing adjacent scripts",
            "next_action": "build dry-run first; no long run without explicit command/log workflow",
        },
        {
            "decision": "claim_status",
            "status": "closure_testing_only",
            "evidence": "checkpoint 82 found no fully parent-derived amplitude",
            "next_action": "do not treat empirical success as field-theory proof",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name,
        "readout": "empirical_closure_manifest_ready_not_executed",
        "key_metrics": {
            "test_manifest_rows": counts["test_manifest"],
            "amplitude_policies": counts["amplitude_policy"],
            "baseline_rules": counts["baseline_fairness"],
            "output_contracts": counts["output_contract"],
            "primary_next_test": "cosmo_background_SN_BAO_short_smoke",
        },
        "decision": decision_rows()[0],
        "next_target": "84-closure-test-runner-design.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-empirical-closure-test-manifest"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "test_manifest": (
            test_manifest_rows(),
            [
                "test_id",
                "arena",
                "data_or_proxy",
                "mts_variant",
                "fixed_factors",
                "fitted_factors",
                "ablations",
                "baselines",
                "required_diagnostics",
                "claim_ceiling",
            ],
        ),
        "amplitude_policy": (
            amplitude_policy_rows(),
            ["factor", "default_policy", "required_ablation", "failure_flag"],
        ),
        "baseline_fairness": (
            baseline_fairness_rows(),
            ["baseline_rule", "requirement", "why"],
        ),
        "output_contract": (
            output_contract_rows(),
            ["artifact", "required_columns", "required_for"],
        ),
        "decision": (
            decision_rows(),
            ["decision", "status", "evidence", "next_action"],
        ),
    }

    counts: dict[str, int] = {}
    for table_name, (rows, fieldnames) in tables.items():
        write_csv(result_dir / f"{table_name}.csv", rows, fieldnames)
        counts[table_name] = len(rows)

    status = status_payload(run_dir, counts)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=POST_CHECKPOINT / "runs",
        help="Directory where timestamped run output is written.",
    )
    args = parser.parse_args()

    run_dir = run(args.output_root)
    status = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
