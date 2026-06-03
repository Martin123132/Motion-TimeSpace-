from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "fixed-2over27-vs-kappa-free-cosmology-test-manifest"
STATUS = "fixed_2over27_vs_kappa_free_cosmology_manifest_written_no_scores_or_claims"
CLAIM_CEILING = "test_manifest_only_no_new_empirical_or_theory_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"
B_MEM_FIXED = 2.0 / 27.0


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (
            "frozen branch scorecard",
            ROOT / "144-frozen-branch-empirical-holdout-scorecard.md",
            "existing fixed 2/27 late-time empirical scorecard",
        ),
        (
            "frozen branch evidence table",
            ROOT
            / "runs"
            / "20260531-214500-frozen-branch-empirical-holdout-scorecard"
            / "results"
            / "evidence_scorecard.csv",
            "machine-readable previous late-time evidence card",
        ),
        (
            "no-clock SN BAO reproduction guard",
            ROOT / "173-no-clock-SN-BAO-reproduction-guard.md",
            "existing locked 2/27 SN+BAO reproduction guard",
        ),
        (
            "CMB profiled readiness",
            ROOT / "189-CMB-profiled-shape-residual-and-likelihood-readiness.md",
            "CMB remains profiled/mock-readiness only",
        ),
        (
            "kappa normalization checkpoint",
            ROOT / "255-memory-stress-exchange-normalization-or-kappa-mem-free.md",
            "kappa_mem not derived; kappa-free branch allowed as ablation",
        ),
        (
            "closure branch policy",
            ROOT
            / "runs"
            / "20260601-000072-memory-stress-exchange-normalization-or-kappa-mem-free"
            / "results"
            / "closure_branch_policy.csv",
            "machine-readable fixed/kappa/corridor branch policy",
        ),
        (
            "SN+BAO reproduction runner",
            ROOT / "scripts" / "no_clock_official_likelihood_refresh.py",
            "existing reproduction machinery for locked branch",
        ),
        (
            "BAO-only release runner",
            ROOT / "scripts" / "locked_2over27_BAO_only_release_test.py",
            "existing BAO-only locked release machinery",
        ),
        (
            "CMB profiled readiness runner",
            ROOT / "scripts" / "CMB_profiled_shape_residual_and_likelihood_readiness.py",
            "existing CMB profiled residual machinery",
        ),
    ]
    return [
        {
            "source": source,
            "path": relpath(path),
            "exists": "yes" if path.exists() else "no",
            "use_in_256": use,
        }
        for source, path, use in sources
    ]


def model_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_key": "LCDM",
            "role": "baseline",
            "Bmem_policy": "none",
            "fixed_parameters": "standard baseline only",
            "fitted_parameters": "Omega_m plus shared nuisance/calibration parameters",
            "extra_parameters_vs_fixed_2over27": 0,
            "claim_ceiling": "baseline",
            "required": "yes",
        },
        {
            "model_key": "wCDM",
            "role": "flexible_baseline",
            "Bmem_policy": "none",
            "fixed_parameters": "standard baseline only",
            "fitted_parameters": "Omega_m,w plus shared nuisance/calibration parameters",
            "extra_parameters_vs_fixed_2over27": 1,
            "claim_ceiling": "baseline",
            "required": "yes",
        },
        {
            "model_key": "CPL",
            "role": "flexible_baseline",
            "Bmem_policy": "none",
            "fixed_parameters": "standard baseline only",
            "fitted_parameters": "Omega_m,w0,wa plus shared nuisance/calibration parameters",
            "extra_parameters_vs_fixed_2over27": 2,
            "claim_ceiling": "baseline",
            "required": "yes",
        },
        {
            "model_key": "MTS_fixed_2over27_no_clock",
            "role": "strict_lead_closure",
            "Bmem_policy": f"fixed_Bmem={B_MEM_FIXED:.12f}",
            "fixed_parameters": "p=3,u3=1/4,B_mem=2/27,no global clock,no pair-ruler sidecar",
            "fitted_parameters": "Omega_m plus same nuisance/calibration parameters as baselines",
            "extra_parameters_vs_fixed_2over27": 0,
            "claim_ceiling": "empirical closure only",
            "required": "yes",
        },
        {
            "model_key": "MTS_kappa_free_no_clock",
            "role": "amplitude_ablation",
            "Bmem_policy": "B_mem=kappa_mem*(2/27); kappa_mem fitted",
            "fixed_parameters": "p=3,u3=1/4,no global clock,no pair-ruler sidecar",
            "fitted_parameters": "Omega_m,kappa_mem plus same nuisance/calibration parameters",
            "extra_parameters_vs_fixed_2over27": 1,
            "claim_ceiling": "phenomenological ablation only",
            "required": "yes",
        },
        {
            "model_key": "MTS_free_Bmem_no_clock",
            "role": "legacy_amplitude_ablation",
            "Bmem_policy": "B_mem fitted directly",
            "fixed_parameters": "p=3,u3=1/4,no global clock,no pair-ruler sidecar",
            "fitted_parameters": "Omega_m,B_mem plus same nuisance/calibration parameters",
            "extra_parameters_vs_fixed_2over27": 1,
            "claim_ceiling": "phenomenological ablation only",
            "required": "optional_equivalence_check",
        },
        {
            "model_key": "MTS_Bmem_zero",
            "role": "negative_control",
            "Bmem_policy": "B_mem=0",
            "fixed_parameters": "p=3,u3=1/4,B_mem=0",
            "fitted_parameters": "Omega_m plus same nuisance/calibration parameters",
            "extra_parameters_vs_fixed_2over27": 0,
            "claim_ceiling": "control only",
            "required": "yes",
        },
    ]


def arena_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "SN_BAO_T7_reproduction",
            "status": "existing_locked_branch_reproduction_guard",
            "primary_question": "does kappa freedom improve enough to pay its parameter tax?",
            "models_required": "LCDM,wCDM,CPL,MTS_fixed_2over27_no_clock,MTS_kappa_free_no_clock,MTS_Bmem_zero",
            "data_rule": "same SN rows/covariance/observable and BAO release for every model",
            "score_rule": "chi2,AIC,BIC,edge flags,residuals",
            "claim_ceiling": "late-time closure only",
        },
        {
            "arena": "no_SH0ES_SN_BAO",
            "status": "must_be_run_as_same_pipeline_split",
            "primary_question": "does fixed 2/27 survive without local-H0 calibration pressure?",
            "models_required": "same as SN_BAO_T7_reproduction",
            "data_rule": "Pantheon shape/nuisance offset branch; BAO unchanged",
            "score_rule": "delta chi2/AIC/BIC against LCDM,wCDM,CPL and fixed-vs-kappa",
            "claim_ceiling": "late-time closure only",
        },
        {
            "arena": "BAO_only_DR1_DR2",
            "status": "existing_locked_BAO_runner_available",
            "primary_question": "does kappa freedom survive release-to-release or just absorb BAO quirks?",
            "models_required": "LCDM,wCDM,CPL,MTS_fixed_2over27_no_clock,MTS_kappa_free_no_clock",
            "data_rule": "DR1 and DR2 reported together; no cherry-pick",
            "score_rule": "release sensitivity, AIC/BIC, residual decomposition",
            "claim_ceiling": "BAO distance closure only",
        },
        {
            "arena": "BAO_Hz_noCMB",
            "status": "existing no-CMB robustness evidence; kappa branch not yet refreshed",
            "primary_question": "does kappa improve H(z) without losing fixed-branch parsimony?",
            "models_required": "LCDM,wCDM,CPL,MTS_fixed_2over27_no_clock,MTS_kappa_free_no_clock",
            "data_rule": "same Hz compilation and BAO covariance; no CMB calibration",
            "score_rule": "delta AIC/BIC and split stability",
            "claim_ceiling": "late-time closure only",
        },
        {
            "arena": "growth_fsigma8_proxy",
            "status": "proxy_only",
            "primary_question": "does fixed/kappa branch create unacceptable growth residuals?",
            "models_required": "LCDM,wCDM,CPL,MTS_fixed_2over27_no_clock,MTS_kappa_free_no_clock",
            "data_rule": "same growth covariance and same high-cs/effective perturbation assumptions",
            "score_rule": "proxy chi2 and subhorizon correction bounds",
            "claim_ceiling": "effective perturbation proxy only",
        },
        {
            "arena": "CMB_profiled_mock_or_readiness",
            "status": "mock/readiness only; no official likelihood claim",
            "primary_question": "does amplitude freedom hide CMB shape tension or genuinely improve matched profile?",
            "models_required": "matched LCDM controls,MTS_fixed_2over27_no_clock,MTS_kappa_free_no_clock",
            "data_rule": "theta/H0 profiling rules fixed before scoring; no official Planck/ACT/SPT claim",
            "score_rule": "shape residuals, mock likelihood readiness, hard CMB bridge flags",
            "claim_ceiling": "CMB diagnostic only",
        },
    ]


def comparison_rule_rows() -> list[dict[str, Any]]:
    return [
        {
            "comparison": "fixed_2over27_vs_LCDM",
            "delta_k": 0,
            "AIC_win_condition": "delta_chi2_vs_LCDM < 0 when parameter counts are equal under same nuisance policy",
            "BIC_win_condition": "delta_chi2_vs_LCDM < 0 when parameter counts are equal under same nuisance policy",
            "interpretation": "fixed branch can win/draw on points if stable and non-edge",
        },
        {
            "comparison": "fixed_2over27_vs_wCDM",
            "delta_k": "wCDM usually has +1 dark-energy parameter",
            "AIC_win_condition": "fixed can lose raw chi2 by up to 2 and still draw/win AIC",
            "BIC_win_condition": "fixed can lose raw chi2 by up to ln(n_eff) and still draw/win BIC",
            "interpretation": "parsimony is legitimate if nuisance policies match",
        },
        {
            "comparison": "kappa_free_vs_fixed_2over27",
            "delta_k": 1,
            "AIC_win_condition": "kappa branch must improve chi2 by more than 2",
            "BIC_win_condition": "kappa branch must improve chi2 by more than ln(n_eff)",
            "interpretation": "otherwise strict fixed 2/27 remains the cleaner lead branch",
        },
        {
            "comparison": "free_Bmem_vs_kappa_free",
            "delta_k": 0,
            "AIC_win_condition": "should be equivalent up to parameterization if kappa prior maps exactly to B_mem prior",
            "BIC_win_condition": "same as AIC; discrepancy signals prior/implementation asymmetry",
            "interpretation": "guards against pretending kappa is more derived than a free amplitude",
        },
        {
            "comparison": "kappa_free_vs_CPL",
            "delta_k": "depends on nuisance policy; usually kappa has fewer shape parameters than CPL",
            "AIC_win_condition": "must be computed with exact parameter counts from run_config",
            "BIC_win_condition": "must be computed with exact n_eff and parameter counts",
            "interpretation": "no hand-wavy victory; record exact dof and n_eff",
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "same_pipeline_for_all_models",
            "pass_condition": "identical rows, covariance, calibration branch, nuisance handling, and convergence settings",
            "fail_condition": "any MTS-only or baseline-only data/nuisance asymmetry",
        },
        {
            "gate": "fixed_branch_not_prior_edge",
            "pass_condition": "fixed branch has no hidden fitted amplitude and no nuisance edge pathology unique to MTS",
            "fail_condition": "locked branch depends on hidden edge or omitted failure row",
        },
        {
            "gate": "kappa_parameter_tax_paid",
            "pass_condition": "kappa-free improves chi2 by >2 for AIC and >ln(n_eff) for BIC versus fixed branch",
            "fail_condition": "kappa improves raw chi2 but loses information criteria",
        },
        {
            "gate": "baselines_reported_symmetrically",
            "pass_condition": "LCDM,wCDM,CPL convergence/edge failures reported with same severity as MTS failures",
            "fail_condition": "baseline failures hidden or MTS failures over-interpreted without baseline context",
        },
        {
            "gate": "CMB_claim_block",
            "pass_condition": "CMB rows remain diagnostic/mock/readiness until official likelihood and perturbation bridge exist",
            "fail_condition": "any CMB pass/support wording from profiled or compressed diagnostics",
        },
        {
            "gate": "theory_claim_block",
            "pass_condition": "fixed/kappa results do not promote B_mem derivation, parent action, local GR, or perturbations",
            "fail_condition": "any score is described as parent-derived amplitude evidence",
        },
    ]


def command_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "command_id": "reproduce_locked_SN_BAO_existing",
            "status": "existing_runner",
            "command": "python scripts/no_clock_official_likelihood_refresh.py --mode reproduce --arena SN-BAO-T7 --assert-no-sidecar --timestamp <timestamp> --source-run runs/20260531-235959-no-clock-official-source-refresh --reference-tolerance 1e-8",
            "expected_output": "reproduces fixed 2/27 reference matrix; no kappa fit",
        },
        {
            "command_id": "new_fixed_vs_kappa_SN_BAO_dryrun",
            "status": "needs_runner_next",
            "command": "python scripts/fixed_vs_kappa_cosmology_runner.py --phase dry-run --arena SN-BAO-T7 --models fixed_2over27,kappa_free,LCDM,wCDM,CPL",
            "expected_output": "data schema plus model matrix; no long fit",
        },
        {
            "command_id": "new_fixed_vs_kappa_SN_BAO_short",
            "status": "after_dryrun_only",
            "command": "python scripts/fixed_vs_kappa_cosmology_runner.py --phase short-smoke --arena SN-BAO-T7 --max-iter 200",
            "expected_output": "fit_summary, baseline comparison, kappa penalty table",
        },
        {
            "command_id": "BAO_only_release_refresh",
            "status": "existing_locked_runner_needs_kappa_extension",
            "command": "python scripts/locked_2over27_BAO_only_release_test.py --dry-run",
            "expected_output": "DR1/DR2 locked branch check; kappa extension later",
        },
        {
            "command_id": "CMB_profiled_readiness_no_claim",
            "status": "existing_diagnostic_runner",
            "command": "python scripts/CMB_profiled_shape_residual_and_likelihood_readiness.py --timestamp <timestamp>",
            "expected_output": "profiled residuals only; no official likelihood claim",
        },
    ]


def output_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "artifact": "fit_summary.csv",
            "required_columns": "arena,model,chi2,n_eff,k_params,AIC,BIC,converged,prior_edge_flag,claim_ceiling",
            "why_required": "information criteria and edge discipline",
        },
        {
            "artifact": "fixed_vs_kappa_penalty.csv",
            "required_columns": "arena,chi2_fixed,chi2_kappa,delta_chi2,delta_k,AIC_tax_paid,BIC_tax_paid,n_eff",
            "why_required": "prevents treating kappa freedom as free evidence",
        },
        {
            "artifact": "baseline_comparison.csv",
            "required_columns": "arena,baseline,same_data,same_nuisance,delta_chi2,delta_AIC,delta_BIC,baseline_failure_flags",
            "why_required": "fair points-card comparison",
        },
        {
            "artifact": "residuals.csv",
            "required_columns": "arena,dataset,model,x,observed,predicted,residual,normalized_residual",
            "why_required": "diagnose whether wins are shape or calibration artifacts",
        },
        {
            "artifact": "status.json",
            "required_columns": "status,claim_ceiling,stable_evidence_allowed,kappa_promoted,fixed_branch_promoted,next_action",
            "why_required": "machine-readable claim control",
        },
    ]


def claim_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "fixed 2/27 branch is the strict lead test branch",
            "status": "allowed",
            "reason": "B_mem remains fixed, no kappa freedom, no sidecar clock/pair-ruler law",
        },
        {
            "claim": "kappa-free branch is evidence of parent amplitude derivation",
            "status": "forbidden",
            "reason": "kappa_mem is explicitly not derived",
        },
        {
            "claim": "kappa-free branch may be tested as an ablation",
            "status": "allowed",
            "reason": "useful diagnostic if it pays AIC/BIC parameter tax",
        },
        {
            "claim": "CMB passes from profiled/compressed diagnostics",
            "status": "forbidden",
            "reason": "official likelihood and perturbation bridge are not cleared",
        },
        {
            "claim": "baseline failures matter too",
            "status": "required",
            "reason": "if jackknife/data splits break all comparable theories, the pipeline/data split is suspect",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_register_rows())
    model_count = len(model_matrix_rows())
    arena_count = len(arena_matrix_rows())
    kappa_rules = sum("kappa" in row["comparison"] for row in comparison_rule_rows())
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "promotion_allowed": "false",
        },
        {
            "gate": "model matrix includes fixed and kappa branches",
            "status": "pass" if model_count >= 7 else "fail",
            "evidence": f"model_rows={model_count}",
            "promotion_allowed": "test only",
        },
        {
            "gate": "multi-arena test matrix written",
            "status": "pass" if arena_count >= 6 else "fail",
            "evidence": f"arena_rows={arena_count}",
            "promotion_allowed": "test only",
        },
        {
            "gate": "kappa parameter penalty declared",
            "status": "pass" if kappa_rules >= 2 else "fail",
            "evidence": f"kappa_comparison_rows={kappa_rules}",
            "promotion_allowed": "ablation only",
        },
        {
            "gate": "new empirical score claimed",
            "status": "fail",
            "evidence": "manifest only; no new fit executed",
            "promotion_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "meaning": (
                "The next empirical stage is frozen: fixed B_mem=2/27 remains the strict lead closure, "
                "while B_mem=kappa_mem(2/27) is an amplitude ablation that must pay one-parameter AIC/BIC tax. "
                "All comparisons must use identical data splits, nuisance/calibration handling, residual outputs, "
                "and symmetric failure reporting against LCDM, wCDM, and CPL. This manifest creates no new score "
                "and permits no theory or CMB promotion."
            ),
            "fixed_Bmem": f"{B_MEM_FIXED:.12f}",
            "kappa_promoted": "false",
            "next_target": "257-fixed-vs-kappa-free-SN-BAO-dryrun-runner.md",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_id = f"{timestamp}-{RUN_SLUG}"
    run_dir = ROOT / "runs" / run_id
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (
            source_register_rows(),
            ["source", "path", "exists", "use_in_256"],
        ),
        "model_matrix.csv": (
            model_matrix_rows(),
            [
                "model_key",
                "role",
                "Bmem_policy",
                "fixed_parameters",
                "fitted_parameters",
                "extra_parameters_vs_fixed_2over27",
                "claim_ceiling",
                "required",
            ],
        ),
        "arena_matrix.csv": (
            arena_matrix_rows(),
            ["arena", "status", "primary_question", "models_required", "data_rule", "score_rule", "claim_ceiling"],
        ),
        "comparison_rules.csv": (
            comparison_rule_rows(),
            ["comparison", "delta_k", "AIC_win_condition", "BIC_win_condition", "interpretation"],
        ),
        "acceptance_gates.csv": (
            acceptance_gate_rows(),
            ["gate", "pass_condition", "fail_condition"],
        ),
        "command_templates.csv": (
            command_template_rows(),
            ["command_id", "status", "command", "expected_output"],
        ),
        "output_contract.csv": (
            output_contract_rows(),
            ["artifact", "required_columns", "why_required"],
        ),
        "claim_policy_after_256.csv": (
            claim_policy_rows(),
            ["claim", "status", "reason"],
        ),
        "claim_gate_results.csv": (
            claim_gate_rows(),
            ["gate", "status", "evidence", "promotion_allowed"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "lead_branch", "meaning", "fixed_Bmem", "kappa_promoted", "next_target"],
        ),
    }

    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "missing_sources": sum(row["exists"] != "yes" for row in source_register_rows()),
        "fixed_Bmem": f"{B_MEM_FIXED:.12f}",
        "kappa_free_branch": "ablation_only",
        "kappa_AIC_tax_delta_chi2": 2,
        "kappa_BIC_tax_delta_chi2": "ln(n_eff)",
        "example_BIC_tax_n100": f"{math.log(100):.6f}",
        "new_scores_generated": False,
        "promotion_allowed": False,
        "next_target": "257-fixed-vs-kappa-free-SN-BAO-dryrun-runner.md",
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return status_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build checkpoint 256: fixed 2/27 vs kappa-free cosmology test manifest.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
