#!/usr/bin/env python3
"""Plan the fair empirical scorecard for the canonical_R_closure branch.

This is a dry planning artifact. It does not run long fits. It converts the
post-theorem-demotion branch into a labelled empirical retest matrix with clear
claim ceilings and command recipes.
"""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RUNS_ROOT = POST_CHECKPOINT / "runs"

SOURCE_CHECKPOINTS = [
    POST_CHECKPOINT / "90-cosmo-model-selection-stability-ledger.md",
    POST_CHECKPOINT / "91-Bmem-p-u3-parent-ownership-gate.md",
    POST_CHECKPOINT / "92-memory-stress-amplitude-prediction-attempt.md",
    POST_CHECKPOINT / "93-Lcg-trace-contrast-owner-gate.md",
    POST_CHECKPOINT / "94-endpoint-relaxation-DeltaR-gate.md",
    POST_CHECKPOINT / "95-trace-coupling-aF-normalization-gate.md",
    POST_CHECKPOINT / "96-parent-R-normalization-contract.md",
    POST_CHECKPOINT / "97-canonical-R-theorem-attempt.md",
    POST_CHECKPOINT / "scripts" / "cosmo_SN_BAO_closure_runner.py",
    POST_CHECKPOINT / "scripts" / "cosmo_model_selection_stability_ledger.py",
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, Any]]:
    role = {
        "90-cosmo-model-selection-stability-ledger.md": "prior scorecard and judging rules",
        "91-Bmem-p-u3-parent-ownership-gate.md": "p/u3/Bmem ownership status",
        "92-memory-stress-amplitude-prediction-attempt.md": "Bmem amplitude corridor",
        "93-Lcg-trace-contrast-owner-gate.md": "eta=1 conditional lock",
        "94-endpoint-relaxation-DeltaR-gate.md": "DeltaR sign/range gate",
        "95-trace-coupling-aF-normalization-gate.md": "a_F=1 canonical viability",
        "96-parent-R-normalization-contract.md": "parent contract and theorem debt",
        "97-canonical-R-theorem-attempt.md": "canonical_R_closure demotion",
        "cosmo_SN_BAO_closure_runner.py": "fit runner for SN+BAO branches",
        "cosmo_model_selection_stability_ledger.py": "scorecard ledger aggregator",
    }
    return [{"source": str(path), "exists": path.exists(), "role": role[path.name]} for path in SOURCE_CHECKPOINTS]


def branch_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_label": "canonical_R_closure",
            "numeric_runner_model": "MTS_fixed_p3_u3quarter",
            "fixed_or_conditional_choices": "p=3; u3=1/4; eta=1; a_F=1",
            "fitted_quantities": "Omega_m; B_mem; SN nuisance offset/calibration",
            "derived_or_conditional": "p=3 conditional; u3=1/4 conditional; eta=1 conditional",
            "explicit_closure_debt": "a_F=1; R unit scale; DeltaR endpoint value; B_mem amplitude",
            "claim_ceiling": "empirical_closure_scorecard_only",
        },
        {
            "branch_label": "MTS_Bmem_zero",
            "numeric_runner_model": "MTS_Bmem_zero",
            "fixed_or_conditional_choices": "p=3; u3=1/4; B_mem=0",
            "fitted_quantities": "Omega_m; SN nuisance offset/calibration",
            "derived_or_conditional": "negative control using same shape with zero memory amplitude",
            "explicit_closure_debt": "tests whether nonzero memory amplitude is doing work",
            "claim_ceiling": "negative_control_only",
        },
        {
            "branch_label": "MTS_fitted_p",
            "numeric_runner_model": "MTS_fitted_p",
            "fixed_or_conditional_choices": "u3=1/4; p fitted",
            "fitted_quantities": "Omega_m; p; B_mem; SN nuisance offset/calibration",
            "derived_or_conditional": "ablation only",
            "explicit_closure_debt": "shape freedom cannot support canonical branch if it edge-hits",
            "claim_ceiling": "ablation_only",
        },
        {
            "branch_label": "MTS_fitted_u3",
            "numeric_runner_model": "MTS_fitted_u3",
            "fixed_or_conditional_choices": "p=3; u3 fitted",
            "fitted_quantities": "Omega_m; u3; B_mem; SN nuisance offset/calibration",
            "derived_or_conditional": "ablation only",
            "explicit_closure_debt": "free-u3 edge-hitting is a warning, not evidence",
            "claim_ceiling": "ablation_only",
        },
    ]


def retest_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "T0_dry_run_shape_check",
            "priority": 0,
            "sn_observable": "mb-corr",
            "sn_covariance_mode": "full",
            "sn_rows": "full",
            "bao_release": "DESI_DR2_primary",
            "include_mts_ablations": False,
            "purpose": "prove data shapes and config before long scoring",
            "acceptance": "all data shapes pass; no fit run required",
        },
        {
            "test_id": "T1_clean_primary_fullcov",
            "priority": 1,
            "sn_observable": "mb-corr",
            "sn_covariance_mode": "full",
            "sn_rows": "full",
            "bao_release": "DESI_DR2_primary",
            "include_mts_ablations": False,
            "purpose": "main no-SH0ES full-covariance scorecard",
            "acceptance": "canonical_R_closure converges, no edge hit, compare to LCDM/wCDM/CPL by chi2/AIC/BIC",
        },
        {
            "test_id": "T2_clean_primary_with_ablations",
            "priority": 2,
            "sn_observable": "mb-corr",
            "sn_covariance_mode": "full",
            "sn_rows": "full",
            "bao_release": "DESI_DR2_primary",
            "include_mts_ablations": True,
            "purpose": "separate fixed-closure performance from shape rescue",
            "acceptance": "fitted-p/u3 branches cannot be used as evidence if edge-hit or overfit",
        },
        {
            "test_id": "T3_diagonal_covariance_sensitivity",
            "priority": 3,
            "sn_observable": "mb-corr",
            "sn_covariance_mode": "diagonal",
            "sn_rows": "full",
            "bao_release": "DESI_DR2_primary",
            "include_mts_ablations": False,
            "purpose": "check whether full-cov result is covariance-sensitive",
            "acceptance": "diagonal branch may inform robustness but cannot outrank full-covariance primary",
        },
        {
            "test_id": "T4_small_sample_reproduction",
            "priority": 4,
            "sn_observable": "mb-corr",
            "sn_covariance_mode": "full",
            "sn_rows": "250",
            "bao_release": "DESI_DR2_primary",
            "include_mts_ablations": True,
            "purpose": "reproduce older short-smoke behaviour and edge flags",
            "acceptance": "small sample is diagnostic only, not decisive",
        },
        {
            "test_id": "T5_SH0ES_pressure_branch",
            "priority": 5,
            "sn_observable": "mu-sh0es",
            "sn_covariance_mode": "diagonal",
            "sn_rows": "250",
            "bao_release": "DESI_DR2_primary",
            "include_mts_ablations": True,
            "purpose": "stress branch under local-H0 calibration pressure",
            "acceptance": "never use SH0ES-pressure improvement as standalone support",
        },
        {
            "test_id": "T6_BAO_release_sensitivity",
            "priority": 6,
            "sn_observable": "mb-corr",
            "sn_covariance_mode": "full",
            "sn_rows": "250",
            "bao_release": "DESI_DR1_primary",
            "include_mts_ablations": True,
            "purpose": "probe BAO-release sensitivity already seen in DR1",
            "acceptance": "DR1 weakening triggers repair queue, not cherry-picking",
        },
    ]


def scorecard_rule_rows() -> list[dict[str, Any]]:
    return [
        {
            "rule": "primary_baselines",
            "requirement": "Always score canonical_R_closure against fitted LCDM, fitted wCDM, and fitted CPL.",
            "reason": "Avoid making MTS fight only the easiest opponent.",
        },
        {
            "rule": "information_criteria",
            "requirement": "Report chi2, AIC, and BIC deltas against every baseline.",
            "reason": "Close rounds need multiple judge cards, not a single knockout metric.",
        },
        {
            "rule": "edge_flags_block_evidence",
            "requirement": "Any MTS edge hit or failed convergence blocks stable-evidence language.",
            "reason": "A branch leaning on prior edges is not a clean points win.",
        },
        {
            "rule": "baseline_edge_flags_recorded",
            "requirement": "Baseline edge hits are recorded as unclean baseline rounds, not silently awarded.",
            "reason": "Fair comparison means GR/dark-energy baselines get scrutinized too.",
        },
        {
            "rule": "full_covariance_primary",
            "requirement": "No-SH0ES full-sample full-covariance DR2 is the primary background scorecard.",
            "reason": "Diagonal and small-sample branches are useful diagnostics but weaker evidence.",
        },
        {
            "rule": "amplitude_claim_ceiling",
            "requirement": "B_mem maps to DeltaR=3 B_mem under eta=1,a_F=1, but remains fitted-output inherited.",
            "reason": "Canonical_R_closure is not an amplitude prediction.",
        },
        {
            "rule": "draws_are_allowed",
            "requirement": "A close AIC/BIC draw or narrow points result keeps the branch alive if it is edge-free.",
            "reason": "The target is a serious unified closure contender, not mandatory knockout dominance.",
        },
    ]


def command_rows() -> list[dict[str, Any]]:
    python = POST_CHECKPOINT / ".venv-score" / "Scripts" / "python.exe"
    runner = POST_CHECKPOINT / "scripts" / "cosmo_SN_BAO_closure_runner.py"
    ledger = POST_CHECKPOINT / "scripts" / "cosmo_model_selection_stability_ledger.py"
    base = f'& "{python}" "{runner}"'
    ledger_cmd = f'& "{python}" "{ledger}"'
    return [
        {
            "step": "dry_run_primary",
            "runs_long": False,
            "command": f'{base} --phase dry-run --sn-observable mb-corr --sn-covariance-mode full --sn-max-rows 0 --bao-label DESI_DR2_primary',
            "notes": "Run before any long fit; checks shapes/config only.",
        },
        {
            "step": "primary_fullcov_fit",
            "runs_long": True,
            "command": f'{base} --phase short-smoke --sn-observable mb-corr --sn-covariance-mode full --sn-max-rows 0 --bao-label DESI_DR2_primary --max-iter 120',
            "notes": "Main canonical_R_closure scorecard branch.",
        },
        {
            "step": "primary_fullcov_ablations",
            "runs_long": True,
            "command": f'{base} --phase short-smoke --sn-observable mb-corr --sn-covariance-mode full --sn-max-rows 0 --bao-label DESI_DR2_primary --include-mts-ablations --max-iter 120',
            "notes": "Separates fixed closure from fitted-p/u3 rescue.",
        },
        {
            "step": "diagonal_sensitivity",
            "runs_long": True,
            "command": f'{base} --phase short-smoke --sn-observable mb-corr --sn-covariance-mode diagonal --sn-max-rows 0 --bao-label DESI_DR2_primary --max-iter 120',
            "notes": "Diagnostic only; full covariance remains primary.",
        },
        {
            "step": "ledger_after_runs",
            "runs_long": False,
            "command": ledger_cmd,
            "notes": "Needs update if new run IDs are added to the ledger selected-run list.",
        },
    ]


def claim_guardrail_rows() -> list[dict[str, Any]]:
    return [
        {
            "allowed": "canonical_R_closure is an edge-free labelled closure branch if the fit converges away from priors.",
            "forbidden": "canonical_R_closure is a derived field-theory prediction.",
        },
        {
            "allowed": "B_mem can be translated to DeltaR=3B_mem under eta=1,a_F=1 for theorem-target bookkeeping.",
            "forbidden": "MTS predicts DeltaR or B_mem from the parent action.",
        },
        {
            "allowed": "AIC/BIC wins over wCDM/CPL can be called clean/style points wins if edge-free.",
            "forbidden": "MTS has beaten cosmology or proven dark energy replacement.",
        },
        {
            "allowed": "A narrow LCDM BIC loss is a keep-working result if MTS remains competitive elsewhere.",
            "forbidden": "Ignore LCDM BIC because MTS is more unified.",
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "data_shapes_pass",
            "result_needed": "dry-run passes for primary no-SH0ES full-covariance full sample",
            "blocks_if_failed": True,
        },
        {
            "gate": "primary_models_converge",
            "result_needed": "LCDM, wCDM, CPL, canonical_R_closure, and Bmem-zero control converge",
            "blocks_if_failed": True,
        },
        {
            "gate": "canonical_branch_non_edge",
            "result_needed": "canonical_R_closure has no prior-edge flag",
            "blocks_if_failed": True,
        },
        {
            "gate": "scorecard_complete",
            "result_needed": "delta chi2/AIC/BIC reported versus LCDM, wCDM, and CPL",
            "blocks_if_failed": True,
        },
        {
            "gate": "amplitude_debt_label_present",
            "result_needed": "all result prose says fitted amplitude/closure, not derived amplitude",
            "blocks_if_failed": True,
        },
        {
            "gate": "future_theory_target_recorded",
            "result_needed": "B_mem translated to DeltaR target only as future theorem target",
            "blocks_if_failed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "next_work_status",
            "value": "canonical_R_closure_scorecard_plan_written",
        },
        {
            "decision": "primary_empirical_branch",
            "value": "no_SH0ES_full_sample_full_covariance_DR2",
        },
        {
            "decision": "branch_alias",
            "value": "MTS_fixed_p3_u3quarter_numeric_model_is_canonical_R_closure_when_claim_ceiling_is_enforced",
        },
        {
            "decision": "claim_ceiling",
            "value": "empirical_closure_scorecard_only",
        },
        {
            "decision": "next_target",
            "value": "run_T0_dry_run_then_primary_fullcov_fit_when_compute_time_is_available",
        },
    ]


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-canonical-R-closure-scorecard-plan"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_table = source_rows()
    if not all(row["exists"] for row in source_table):
        missing = [row["source"] for row in source_table if not row["exists"]]
        raise FileNotFoundError(f"Missing scorecard-plan sources: {missing}")

    write_csv(results_dir / "source_checkpoint_register.csv", source_table, ["source", "exists", "role"])
    write_csv(
        results_dir / "canonical_branch_policy.csv",
        branch_policy_rows(),
        [
            "branch_label",
            "numeric_runner_model",
            "fixed_or_conditional_choices",
            "fitted_quantities",
            "derived_or_conditional",
            "explicit_closure_debt",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "fair_retest_matrix.csv",
        retest_matrix_rows(),
        [
            "test_id",
            "priority",
            "sn_observable",
            "sn_covariance_mode",
            "sn_rows",
            "bao_release",
            "include_mts_ablations",
            "purpose",
            "acceptance",
        ],
    )
    write_csv(results_dir / "scorecard_rules.csv", scorecard_rule_rows(), ["rule", "requirement", "reason"])
    write_csv(results_dir / "dry_run_and_fit_commands.csv", command_rows(), ["step", "runs_long", "command", "notes"])
    write_csv(results_dir / "claim_language_guardrails.csv", claim_guardrail_rows(), ["allowed", "forbidden"])
    write_csv(
        results_dir / "acceptance_gates.csv",
        acceptance_gate_rows(),
        ["gate", "result_needed", "blocks_if_failed"],
    )
    write_csv(results_dir / "decision.csv", decision_rows(), ["decision", "value"])

    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "readout": "canonical_R_closure_scorecard_plan_written",
        "primary_branch": "no_SH0ES_full_sample_full_covariance_DR2",
        "numeric_model_alias": "MTS_fixed_p3_u3quarter -> canonical_R_closure",
        "planned_tests": len(retest_matrix_rows()),
        "runs_started": False,
        "stable_evidence_allowed": False,
        "promotion_allowed": False,
        "next_action": "run T0 dry-run first, then primary full-covariance fit when compute time is available",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
