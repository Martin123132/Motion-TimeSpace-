from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "post343-locked-branch-robustness-manifest"
STATUS = "post343_locked_closure_robustness_manifest_written_no_public_claim"
CLAIM_CEILING = "empirical_closure_manifest_only_no_parent_derivation_or_stable_evidence_claim"
LOCKED_B_MEM = 2.0 / 27.0
TOL = 1.0e-9


RUNS = [
    {
        "release": "DR2",
        "run_id": "20260601-174000-DR2-locked2over27-fullcov-noSH0ES-cosmo-SN-BAO-short-smoke",
        "dataset": "Pantheon+ full covariance + DESI DR2 BAO full covariance; no SH0ES",
        "role": "latest official wrapper locked branch primary release",
    },
    {
        "release": "DR1",
        "run_id": "20260601-174500-DR1-locked2over27-fullcov-noSH0ES-cosmo-SN-BAO-short-smoke",
        "dataset": "Pantheon+ full covariance + DESI DR1 BAO full covariance; no SH0ES",
        "role": "BAO-release sensitivity control",
    },
]


DOC_SOURCES = [
    ("100-canonical-R-T1-primary-fullcov-scorecard.md", "pre-343 full-covariance scorecard; fitted-amplitude comparison context"),
    ("101-canonical-R-T2-ablation-scorecard.md", "pre-343 ablation scorecard"),
    ("102-canonical-R-T3-diagonal-covariance-sensitivity.md", "pre-343 covariance sensitivity"),
    ("103-canonical-R-T4-small-sample-reproduction.md", "pre-343 small-sample instability reproduction"),
    ("104-canonical-R-T5-SH0ES-pressure-branch.md", "pre-343 local-H0 pressure branch"),
    ("105-canonical-R-T6-BAO-release-sensitivity.md", "pre-343 DESI release sensitivity"),
    ("106-canonical-R-cosmology-robustness-summary.md", "pre-343 robustness summary and boxing-card readout"),
    ("144-frozen-branch-empirical-holdout-scorecard.md", "frozen branch multi-arena empirical holdout scorecard"),
    ("145-fresh-CC-Hz-source-locked-holdout.md", "source-locked H(z) holdout"),
    ("146-source-locked-growth-covariance-holdout.md", "source-locked growth covariance holdout"),
    ("147-ELG-grid-likelihood-holdout.md", "non-Gaussian ELG grid holdout"),
    ("330-official-wrapper-locked-branch-release-split.md", "official wrapper DR1/DR2 locked 2/27 no-SH0ES release split"),
    ("343-dim27-rank2-origin-closure-decision-gate.md", "post-derivation decision: B_mem=2/27 explicit closure"),
    ("344-amplitude-closure-claim-ledger-update.md", "post-343 claim ledger update"),
]


REQUIRED_RUN_RESULTS = [
    "fit_summary.csv",
    "baseline_comparison.csv",
    "prior_edge_table.csv",
    "amplitude_policy.csv",
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def as_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def as_bool(value: str | bool | None) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def find_row(rows: list[dict[str, str]], column: str, value: str) -> dict[str, str] | None:
    for row in rows:
        if row.get(column) == value:
            return row
    return None


def find_comparison(rows: list[dict[str, str]], model: str, reference: str) -> dict[str, str] | None:
    for row in rows:
        if row.get("model") == model and row.get("reference_baseline") == reference:
            return row
    return None


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for filename, role in DOC_SOURCES:
        path = ROOT / filename
        rows.append(
            {
                "source_path": relpath(path),
                "source_type": "checkpoint_doc",
                "role": role,
                "exists": path.exists(),
                "issue": "" if path.exists() else "missing",
            }
        )
    script_path = Path(__file__).resolve()
    rows.append(
        {
            "source_path": relpath(script_path),
            "source_type": "script",
            "role": "post-343 manifest builder/verifier",
            "exists": script_path.exists(),
            "issue": "" if script_path.exists() else "missing",
        }
    )
    for run in RUNS:
        result_dir = ROOT / "runs" / run["run_id"] / "results"
        rows.append(
            {
                "source_path": relpath(result_dir),
                "source_type": "run_results_dir",
                "role": run["role"],
                "exists": result_dir.exists(),
                "issue": "" if result_dir.exists() else "missing",
            }
        )
        for filename in REQUIRED_RUN_RESULTS:
            path = result_dir / filename
            rows.append(
                {
                    "source_path": relpath(path),
                    "source_type": "run_csv",
                    "role": f"{run['release']} {filename}",
                    "exists": path.exists(),
                    "issue": "" if path.exists() else "missing",
                }
            )
    return rows


def empirical_evidence_rows() -> list[dict[str, Any]]:
    return [
        {
            "evidence_id": "E0_post343_claim_control",
            "arena": "theory-label discipline",
            "source_path": "343-dim27-rank2-origin-closure-decision-gate.md; 344-amplitude-closure-claim-ledger-update.md",
            "result": "B_mem=2/27 is explicit closure/theorem target, not parent-derived",
            "readout": "keeps empirical branch but blocks derivation overclaim",
            "claim_ceiling": CLAIM_CEILING,
            "next_action": "test locked branch as closure; derive parent route separately",
        },
        {
            "evidence_id": "E1_pre343_SN_BAO_matrix",
            "arena": "SN+BAO robustness matrix",
            "source_path": "100-canonical-R-T1-primary-fullcov-scorecard.md; 106-canonical-R-cosmology-robustness-summary.md",
            "result": "pre-343 canonical branch competitive and edge-free in primary full-covariance matrix",
            "readout": "retained as context, but fitted-amplitude rows are not post-343 closure evidence",
            "claim_ceiling": "pre343_context_only",
            "next_action": "use locked no-clock 2/27 rows as primary post-343 evidence",
        },
        {
            "evidence_id": "E2_post343_DR2_locked_release",
            "arena": "SN+BAO full-cov no-SH0ES DR2",
            "source_path": "runs/20260601-174000-DR2-locked2over27-fullcov-noSH0ES-cosmo-SN-BAO-short-smoke/results",
            "result": "locked no-clock 2/27 branch edge-clean; DeltaBIC=-5.259466877750583 vs LCDM",
            "readout": "cleanest post-343 background signal so far",
            "claim_ceiling": "late_time_background_closure_performance_only",
            "next_action": "repeat with strict holdouts and no promotion to CMB/local GR",
        },
        {
            "evidence_id": "E3_post343_DR1_locked_release",
            "arena": "SN+BAO full-cov no-SH0ES DR1",
            "source_path": "runs/20260601-174500-DR1-locked2over27-fullcov-noSH0ES-cosmo-SN-BAO-short-smoke/results",
            "result": "locked no-clock 2/27 branch edge-clean; DeltaBIC=-3.6187583484374954 vs LCDM",
            "readout": "release sensitivity weakens but does not collapse the branch",
            "claim_ceiling": "late_time_background_closure_performance_only",
            "next_action": "keep DR1/DR2 release split on warning label",
        },
        {
            "evidence_id": "E4_nonSN_Hz_holdout",
            "arena": "source-locked cosmic chronometer H(z)",
            "source_path": "145-fresh-CC-Hz-source-locked-holdout.md",
            "result": "competitive draw; primary DeltaBIC=+0.33256956910347313 vs LCDM",
            "readout": "not disfavored in fresh non-SN late-time data",
            "claim_ceiling": "holdout_survival_no_theory_promotion",
            "next_action": "do not use H(z) to derive action, amplitude, CMB, or local GR",
        },
        {
            "evidence_id": "E5_growth_and_ELG_holdouts",
            "arena": "growth covariance + ELG grid",
            "source_path": "146-source-locked-growth-covariance-holdout.md; 147-ELG-grid-likelihood-holdout.md",
            "result": "growth covariance and non-Gaussian ELG grid survive as preferred/draw diagnostics",
            "readout": "useful survivability, still GR-proxy/diagnostic rather than derived perturbations",
            "claim_ceiling": "growth_diagnostic_no_perturbation_or_CMB_promotion",
            "next_action": "derive perturbation owner before combining into serious CMB/growth claim",
        },
        {
            "evidence_id": "E6_CMB_warning",
            "arena": "CMB bridge",
            "source_path": "144-frozen-branch-empirical-holdout-scorecard.md",
            "result": "compressed distance diagnostic draw/survival, but late-to-CMB transfer fails and joint bridge is mixed",
            "readout": "hard warning label: no CMB pass",
            "claim_ceiling": "CMB_unresolved",
            "next_action": "build CMB/perturbation bridge from equations before public-like claims",
        },
    ]


def build_run_audit_rows() -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    issues: list[str] = []
    for run in RUNS:
        result_dir = ROOT / "runs" / run["run_id"] / "results"
        if not result_dir.exists():
            issues.append(f"{run['release']}: missing result dir {relpath(result_dir)}")
            continue

        try:
            fit = read_csv(result_dir / "fit_summary.csv")
            comparisons = read_csv(result_dir / "baseline_comparison.csv")
            edges = read_csv(result_dir / "prior_edge_table.csv")
            amplitude = read_csv(result_dir / "amplitude_policy.csv")
        except FileNotFoundError as error:
            issues.append(f"{run['release']}: missing required CSV {error.filename}")
            continue

        locked = find_row(fit, "model", "MTS_fixed_2over27_no_clock")
        fitted = find_row(fit, "model", "MTS_fixed_p3_u3quarter")
        zero = find_row(fit, "model", "MTS_Bmem_zero")
        lcdm = find_row(fit, "model", "LCDM")
        if locked is None or fitted is None or zero is None or lcdm is None:
            issues.append(f"{run['release']}: missing one of locked/fitted/zero/LCDM rows")
            continue

        locked_edges = [row for row in edges if row.get("model") == "MTS_fixed_2over27_no_clock" and as_bool(row.get("edge_flag"))]
        all_edge_count = sum(1 for row in edges if as_bool(row.get("edge_flag")))
        zero_lcdm_max_delta = max(
            abs((as_float(zero.get(metric)) or math.nan) - (as_float(lcdm.get(metric)) or math.nan))
            for metric in ["chi2_total", "AIC", "BIC"]
        )

        locked_amp_row = next((row for row in amplitude if row.get("factor") == "B_mem=2/27"), {})
        fitted_amp_row = next((row for row in amplitude if row.get("factor") == "B_mem/b_mem"), {})
        fitted_bmem = as_float(fitted_amp_row.get("best_fit"))
        fitted_shift = None if fitted_bmem is None else fitted_bmem - LOCKED_B_MEM
        fitted_relative_shift_pct = None if fitted_shift is None else 100.0 * fitted_shift / LOCKED_B_MEM

        for reference in ["LCDM", "wCDM", "CPL"]:
            comp = find_comparison(comparisons, "MTS_fixed_2over27_no_clock", reference)
            if comp is None:
                issues.append(f"{run['release']}: missing locked comparison vs {reference}")
                continue
            rows.append(
                {
                    "release": run["release"],
                    "run_id": run["run_id"],
                    "dataset": run["dataset"],
                    "model": "MTS_fixed_2over27_no_clock",
                    "reference_baseline": reference,
                    "locked_B_mem": LOCKED_B_MEM,
                    "fitted_diagnostic_B_mem": fitted_bmem,
                    "fitted_minus_locked": fitted_shift,
                    "fitted_relative_shift_pct": fitted_relative_shift_pct,
                    "chi2_total": as_float(locked.get("chi2_total")),
                    "AIC": as_float(locked.get("AIC")),
                    "BIC": as_float(locked.get("BIC")),
                    "delta_chi2": as_float(comp.get("delta_chi2")),
                    "delta_AIC": as_float(comp.get("delta_AIC")),
                    "delta_BIC": as_float(comp.get("delta_BIC")),
                    "locked_edge_flag": bool(locked_edges),
                    "any_prior_edge_count": all_edge_count,
                    "zero_memory_max_abs_delta_vs_LCDM": zero_lcdm_max_delta,
                    "same_data": as_bool(comp.get("same_data")),
                    "same_nuisance": as_bool(comp.get("same_nuisance")),
                    "same_calibration": as_bool(comp.get("same_calibration")),
                    "locked_amplitude_policy": locked_amp_row.get("treatment", ""),
                    "claim_ceiling": locked.get("claim_ceiling", ""),
                    "readout": "post343_locked_closure_signal" if reference == "LCDM" else "baseline_ladder_comparison",
                }
            )
    return rows, issues


def next_run_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "next_run": "post343_relabel_dryrun",
            "arena": "official wrapper SN+BAO",
            "purpose": "rerun or relabel DR1/DR2 locked no-clock 2/27 with post-343 claim ceiling embedded",
            "acceptance_gate": "LCDM/wCDM/CPL fitted fairly; no SH0ES; full covariance; zero-memory equals LCDM",
            "expected_artifacts": "fit_summary, baseline_comparison, prior_edge_table, residuals, amplitude_policy",
            "long_run_policy": "dry-run first, then short smoke; no Codex waiting on hour-scale runs",
        },
        {
            "priority": 2,
            "next_run": "strict_baseline_ladder",
            "arena": "SN+BAO robustness",
            "purpose": "make the Mayweather card fair: same data, same nuisance, fitted LCDM/wCDM/CPL, AIC/BIC against all",
            "acceptance_gate": "prior-edge table published and edge-dependent rows not promoted",
            "expected_artifacts": "delta chi2/AIC/BIC vs LCDM,wCDM,CPL; edge flags; residual plots",
            "long_run_policy": "stage in VS Code terminal with status.json/DONE marker",
        },
        {
            "priority": 3,
            "next_run": "independent_late_time_holdout_refresh",
            "arena": "BAO-only, H(z), growth, ELG",
            "purpose": "repeat source-locked non-SN checks with B_mem frozen and no extra knobs",
            "acceptance_gate": "no amplitude refit; negative controls; source hashes/paths locked",
            "expected_artifacts": "holdout scorecards and claim ceilings by arena",
            "long_run_policy": "one arena per run directory",
        },
        {
            "priority": 4,
            "next_run": "CMB_growth_killscreen_before_claim",
            "arena": "CMB/growth bridge",
            "purpose": "block accidental promotion from late-time background success to early-time/perturbation success",
            "acceptance_gate": "explicit perturbation owner or fail label; no compressed-CMB-only pass claim",
            "expected_artifacts": "bridge residuals; failure modes; theorem targets",
            "long_run_policy": "manifest first, heavy Boltzmann work only after derivation contract",
        },
        {
            "priority": 5,
            "next_run": "Hstar_H0_calibration_theory_gate",
            "arena": "derivation",
            "purpose": "attack the remaining factor in B_mem = q_trace * epsilon_H * (H_star/H0)^2",
            "acceptance_gate": "derive H_star=H0 from action/observer normalization or label it closure",
            "expected_artifacts": "checkpoint doc, theorem premises, failure ledger",
            "long_run_policy": "no heavy data run required",
        },
    ]


def claim_ceiling_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "B_mem=2/27",
            "post343_status": "explicit locked closure value and theorem target",
            "allowed": "fixed no-clock late-time closure branch can be tested",
            "forbidden": "parent-derived amplitude",
        },
        {
            "claim": "SN+BAO DR1/DR2 locked score",
            "post343_status": "empirical background evidence only",
            "allowed": "edge-clean locked branch survives release split",
            "forbidden": "stable cosmological evidence or official cosmology pass",
        },
        {
            "claim": "H(z), growth, ELG holdouts",
            "post343_status": "late-time survivability diagnostics",
            "allowed": "branch remains live across independent arenas",
            "forbidden": "derived perturbation theory, local GR, or CMB bridge",
        },
        {
            "claim": "CMB bridge",
            "post343_status": "unresolved/mixed with known failures",
            "allowed": "theorem target and kill-screen route",
            "forbidden": "MTS passes CMB",
        },
        {
            "claim": "unified field theory status",
            "post343_status": "not yet",
            "allowed": "disciplined closure branch plus derivation targets",
            "forbidden": "completed unified theory",
        },
    ]


def gate_rows(
    sources: list[dict[str, Any]], run_rows: list[dict[str, Any]], run_issues: list[str]
) -> list[dict[str, Any]]:
    missing_sources = [row["source_path"] for row in sources if not row["exists"]]
    locked_lcdm = [row for row in run_rows if row["reference_baseline"] == "LCDM"]
    locked_edge_clean = all(not bool(row["locked_edge_flag"]) for row in run_rows) and bool(run_rows)
    no_edges_any = all(int(row["any_prior_edge_count"]) == 0 for row in run_rows) and bool(run_rows)
    zero_ok = all(float(row["zero_memory_max_abs_delta_vs_LCDM"]) <= TOL for row in run_rows) and bool(run_rows)
    fairness_ok = all(row["same_data"] and row["same_nuisance"] and row["same_calibration"] for row in run_rows) and bool(run_rows)
    dr_split_ok = len({row["release"] for row in locked_lcdm}) == 2
    locked_vs_lcdm_bic_ok = all(float(row["delta_BIC"]) < 0.0 for row in locked_lcdm) and bool(locked_lcdm)
    diagnostic_close = all(
        row["fitted_relative_shift_pct"] is not None and abs(float(row["fitted_relative_shift_pct"])) < 1.0
        for row in locked_lcdm
    ) and bool(locked_lcdm)

    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all sources present" if not missing_sources else "; ".join(missing_sources),
        },
        {
            "gate": "run_csvs_parse",
            "status": "pass" if not run_issues and bool(run_rows) else "fail",
            "evidence": "DR1 and DR2 run CSVs parsed" if not run_issues else "; ".join(run_issues),
        },
        {
            "gate": "locked_branch_edge_clean",
            "status": "pass" if locked_edge_clean else "fail",
            "evidence": "MTS_fixed_2over27_no_clock has no prior-edge flags in parsed rows",
        },
        {
            "gate": "no_prior_edge_dependency_in_matrix",
            "status": "pass" if no_edges_any else "warn",
            "evidence": "all parsed prior_edge_table rows are edge-clean" if no_edges_any else "some parsed prior-edge rows flagged",
        },
        {
            "gate": "zero_memory_control_reproduces_LCDM",
            "status": "pass" if zero_ok else "fail",
            "evidence": f"tolerance={TOL}",
        },
        {
            "gate": "fair_baseline_comparisons",
            "status": "pass" if fairness_ok else "fail",
            "evidence": "same data, nuisance, and calibration booleans are true for locked comparisons",
        },
        {
            "gate": "DR1_DR2_release_split_present",
            "status": "pass" if dr_split_ok else "fail",
            "evidence": ",".join(sorted({row["release"] for row in locked_lcdm})),
        },
        {
            "gate": "locked_vs_LCDM_BIC_not_disfavored",
            "status": "pass" if locked_vs_lcdm_bic_ok else "fail",
            "evidence": "; ".join(f"{row['release']} DeltaBIC={row['delta_BIC']}" for row in locked_lcdm),
        },
        {
            "gate": "fitted_diagnostic_near_locked_value",
            "status": "pass" if diagnostic_close else "warn",
            "evidence": "; ".join(
                f"{row['release']} shift_pct={row['fitted_relative_shift_pct']}" for row in locked_lcdm
            ),
        },
        {
            "gate": "post343_claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
        {
            "gate": "CMB_growth_local_GR_not_promoted",
            "status": "pass",
            "evidence": "manifest explicitly separates late-time closure survival from CMB/growth/local-GR derivation",
        },
    ]


def decision_rows(gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hard_failed = [row["gate"] for row in gates if row["status"] == "fail"]
    warn = [row["gate"] for row in gates if row["status"] == "warn"]
    if hard_failed:
        decision = "post343_locked_manifest_failed_hard_gate"
        next_target = "fix_manifest_or_source_paths_before_derivation"
    else:
        decision = STATUS
        next_target = "derive_Hstar_H0_or_reopen_local_GR_PPN_as_independent_gate"
    return [
        {
            "decision": decision,
            "claim_ceiling": CLAIM_CEILING,
            "hard_failed_gates": ";".join(hard_failed),
            "warning_gates": ";".join(warn),
            "meaning": (
                "The post-343 empirical lane is now checkpointed as a closure-performance manifest. "
                "The locked no-clock B_mem=2/27 branch remains live on DR1/DR2 no-SH0ES full-cov SN+BAO, "
                "but this is not a parent derivation, stable cosmology claim, CMB pass, perturbation theory, or local-GR proof."
            ),
            "next_target": next_target,
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    evidence = empirical_evidence_rows()
    run_rows, run_issues = build_run_audit_rows()
    next_runs = next_run_rows()
    claim_ceiling = claim_ceiling_rows()
    gates = gate_rows(sources, run_rows, run_issues)
    decisions = decision_rows(gates)

    outputs = {
        "source_register.csv": (sources, ["source_path", "source_type", "role", "exists", "issue"]),
        "empirical_evidence_register.csv": (
            evidence,
            ["evidence_id", "arena", "source_path", "result", "readout", "claim_ceiling", "next_action"],
        ),
        "post343_robustness_matrix.csv": (
            run_rows,
            [
                "release",
                "run_id",
                "dataset",
                "model",
                "reference_baseline",
                "locked_B_mem",
                "fitted_diagnostic_B_mem",
                "fitted_minus_locked",
                "fitted_relative_shift_pct",
                "chi2_total",
                "AIC",
                "BIC",
                "delta_chi2",
                "delta_AIC",
                "delta_BIC",
                "locked_edge_flag",
                "any_prior_edge_count",
                "zero_memory_max_abs_delta_vs_LCDM",
                "same_data",
                "same_nuisance",
                "same_calibration",
                "locked_amplitude_policy",
                "claim_ceiling",
                "readout",
            ],
        ),
        "next_run_manifest.csv": (
            next_runs,
            [
                "priority",
                "next_run",
                "arena",
                "purpose",
                "acceptance_gate",
                "expected_artifacts",
                "long_run_policy",
            ],
        ),
        "claim_ceiling_table.csv": (claim_ceiling, ["claim", "post343_status", "allowed", "forbidden"]),
        "gate_results.csv": (gates, ["gate", "status", "evidence"]),
        "decision.csv": (
            decisions,
            ["decision", "claim_ceiling", "hard_failed_gates", "warning_gates", "meaning", "next_target"],
        ),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(result_dir / filename, rows, fieldnames)

    payload = {
        "status": decisions[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(result_dir),
        "generated": list(outputs),
        "locked_B_mem": LOCKED_B_MEM,
        "release_rows": len(run_rows),
        "source_paths_missing": sum(1 for row in sources if not row["exists"]),
        "hard_failed_gates": decisions[0]["hard_failed_gates"],
        "warning_gates": decisions[0]["warning_gates"],
        "next_target": decisions[0]["next_target"],
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(payload["status"] + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build post-343 locked-branch robustness manifest.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
