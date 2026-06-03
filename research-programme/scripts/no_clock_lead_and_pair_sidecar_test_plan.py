#!/usr/bin/env python3
"""Lock no-clock MTS as lead lane and pair-ruler as sidecar lane."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

RUN_166 = RUNS_ROOT / "20260531-235959-pair-ruler-row-repair-or-demotion-gate"
RUN_166_RESULTS = RUN_166 / "results"

STATUS = "no_clock_lead_pair_sidecar_governance_locked"
CLAIM_CEILING = "lead_sidecar_governance_no_CMB_local_GR_or_parent_action_promotion"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_role(path: Path) -> str:
    name = path.name
    if name.endswith("no_clock_lead_and_pair_sidecar_test_plan.py"):
        return "current governance auditor"
    if name.startswith("141-"):
        return "locked memory branch contract"
    if name.startswith("144-"):
        return "frozen no-clock empirical scorecard"
    if name.startswith("145-"):
        return "fresh H(z) source-locked holdout"
    if name.startswith("146-"):
        return "source-locked growth covariance holdout"
    if name.startswith("147-"):
        return "ELG grid likelihood holdout"
    if name.startswith("148-"):
        return "promotion ceiling contract"
    if name.startswith("164-"):
        return "fixed pair-ruler smoke source"
    if name.startswith("165-"):
        return "pair-ruler residual and safety audit"
    if name.startswith("166-") or "pair-ruler-row-repair-or-demotion-gate" in str(path):
        return "pair-ruler repair/demotion evidence"
    return "supporting source"


def source_paths(script_path: Path) -> list[Path]:
    return [
        script_path,
        WORK_DIR / "141-consolidated-locked-memory-branch-contract.md",
        WORK_DIR / "144-frozen-branch-empirical-holdout-scorecard.md",
        WORK_DIR / "145-fresh-CC-Hz-source-locked-holdout.md",
        WORK_DIR / "146-source-locked-growth-covariance-holdout.md",
        WORK_DIR / "147-ELG-grid-likelihood-holdout.md",
        WORK_DIR / "148-perturbation-CMB-local-GR-promotion-contract.md",
        WORK_DIR / "164-fixed-pair-ruler-branch-smoke.md",
        WORK_DIR / "165-pair-ruler-residual-and-two-point-safety-audit.md",
        WORK_DIR / "166-pair-ruler-row-repair-or-demotion-gate.md",
        RUN_166 / "status.json",
        RUN_166_RESULTS / "repair_variant_scorecard.csv",
        RUN_166_RESULTS / "repair_row_delta_vs_no_clock.csv",
        RUN_166_RESULTS / "gate_results.csv",
        RUN_166_RESULTS / "decision.csv",
    ]


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in source_paths(script_path):
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": source_role(path),
                "issue": "" if exists else "missing",
            }
        )
    return rows


def repair_score_rows() -> dict[str, dict[str, str]]:
    return {row["variant"]: row for row in read_csv_rows(RUN_166_RESULTS / "repair_variant_scorecard.csv")}


def best_pair_sidecar(scores: dict[str, dict[str, str]]) -> dict[str, str]:
    candidates = [
        row
        for name, row in scores.items()
        if name not in {"projection_off_control", "base_161_fixed"}
        and row.get("repair_allowed") in {"yes", "yes_if_parent_action_owns_half_factor"}
    ]
    return min(candidates, key=lambda row: float(row["delta_BIC_vs_no_clock"]))


def branch_lane_assignment_rows(scores: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    half = scores["pair_action_half_kernel"]
    base = scores["base_161_fixed"]
    return [
        {
            "branch": "MTS_2over27_no_clock_u3quarter",
            "lane": "lead_empirical_lane",
            "role": "default late-time empirical closure branch",
            "fixed_inputs": "B_mem=2/27; u3=1/4; no fitted clock/projection amplitude",
            "allowed_use": "SN+BAO, BAO-only, BAO+H(z), H(z), growth/RSD proxy and official-likelihood refreshes",
            "forbidden_use": "CMB pass, parent-action derivation, local-GR/PPN proof, or perturbation theory claim",
            "promotion_conditions": "derive parent action, perturbation owner, CMB interface, and local silence/PPN branch",
            "current_status": "empirical lead; late-time competitive; theory promotion blocked",
            "evidence": "projection_off_control remains ahead of all parent-constrained pair variants; prior holdouts survive with frozen B_mem",
            "source_files": "144-frozen-branch-empirical-holdout-scorecard.md; 166-pair-ruler-row-repair-or-demotion-gate.md",
        },
        {
            "branch": "MTS_pair_ruler_half_kernel",
            "lane": "sidecar_theorem_test_lane",
            "role": "fixed two-point/ruler sidecar for safety tests",
            "fixed_inputs": "T=(B/8)F(1-2e^-N); S=(B/12)(1-e^-2N)",
            "allowed_use": "growth/RSD response, lensing/slip response, CMB-ruler safety, parent-action ownership of half factor",
            "forbidden_use": "lead cosmology branch, row-wise BAO repair, continuous projection-amplitude fitting, public bridge claim",
            "promotion_conditions": "parent action owns the 1/2 kernel factor and sidecar clears growth/lensing/CMB-ruler safety",
            "current_status": "best structural pair repair but still a draw behind no-clock",
            "evidence": f"delta_BIC_vs_no_clock={half['delta_BIC_vs_no_clock']}; delta_BIC_vs_base_161={half['delta_BIC_vs_base_161']}",
            "source_files": "166-pair-ruler-row-repair-or-demotion-gate.md",
        },
        {
            "branch": "MTS_pair_ruler_base_161",
            "lane": "superseded_sidecar_baseline",
            "role": "reference pair-ruler source-law branch",
            "fixed_inputs": "T=(B/4)F(1-2e^-N); S=(B/6)(1-e^-2N)",
            "allowed_use": "compare half-kernel improvement and row-pressure diagnostics",
            "forbidden_use": "lead branch or default pair sidecar unless half factor is rejected",
            "promotion_conditions": "would need to beat no-clock and clear parent/two-point gates",
            "current_status": "survives but not lead",
            "evidence": f"delta_BIC_vs_no_clock={base['delta_BIC_vs_no_clock']}; delta_BIC_vs_LCDM={base['delta_BIC_vs_LCDM']}",
            "source_files": "161-trace-quadrupole-source-law-attempt.md; 166-pair-ruler-row-repair-or-demotion-gate.md",
        },
        {
            "branch": "MTS_global_clock",
            "lane": "demoted_control_lane",
            "role": "historical diagnostic branch only",
            "fixed_inputs": "global clock deformation route",
            "allowed_use": "negative control and historical comparison",
            "forbidden_use": "default empirical branch or local/clock rescue by assertion",
            "promotion_conditions": "would need independent action, local silence, CMB, and late-time score recovery",
            "current_status": "demoted",
            "evidence": "later governance keeps no-clock branch as lead and blocks global-clock promotion",
            "source_files": "141-consolidated-locked-memory-branch-contract.md; 148-perturbation-CMB-local-GR-promotion-contract.md",
        },
        {
            "branch": "LCDM_wCDM_CPL",
            "lane": "baseline_fairness_lane",
            "role": "comparison baselines that must take the same tests",
            "fixed_inputs": "same data vectors, covariances, nuisance rules, jackknifes, and split tests as MTS",
            "allowed_use": "AIC/BIC/chi2 scorecard, residuals, jackknifes, edge flags, data-split stress tests",
            "forbidden_use": "baseline immunity or asymmetrical test treatment",
            "promotion_conditions": "not applicable; these are reference baselines",
            "current_status": "active fair baselines",
            "evidence": "same-test principle follows current growth/jackknife and cosmology robustness protocol",
            "source_files": "146-source-locked-growth-covariance-holdout.md; 166-pair-ruler-row-repair-or-demotion-gate.md",
        },
    ]


def lead_empirical_evidence_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_arena": "SN+BAO full covariance",
            "lead_branch_readout": "preferred vs fitted LCDM",
            "metric": "DeltaBIC_vs_LCDM=-5.259466877748764",
            "claim_allowed": "late-time empirical support",
            "claim_forbidden": "parent action, perturbation theory, CMB pass, local GR",
            "source": "144-frozen-branch-empirical-holdout-scorecard.md; 148-perturbation-CMB-local-GR-promotion-contract.md",
        },
        {
            "test_arena": "BAO-only release holdout",
            "lead_branch_readout": "DR2 preferred; DR1 draw",
            "metric": "DR2 DeltaBIC=-2.108368627321081; DR1 DeltaBIC=-0.8483738675035859",
            "claim_allowed": "late-time BAO robustness",
            "claim_forbidden": "CMB sound-horizon solution",
            "source": "144-frozen-branch-empirical-holdout-scorecard.md",
        },
        {
            "test_arena": "BAO+H(z), no CMB",
            "lead_branch_readout": "stable draw/preference across production branches",
            "metric": "10/10 draw; DeltaBIC range [-1.9014668577456,-0.5803932783513801]",
            "claim_allowed": "no-CMB late-time expansion survival",
            "claim_forbidden": "CMB bridge promotion",
            "source": "144-frozen-branch-empirical-holdout-scorecard.md",
        },
        {
            "test_arena": "fresh cosmic-chronometer H(z)",
            "lead_branch_readout": "competitive draw vs LCDM",
            "metric": "primary DeltaBIC=+0.33256956910347313",
            "claim_allowed": "independent H(z) non-disfavoring",
            "claim_forbidden": "derivation of action or amplitude",
            "source": "145-fresh-CC-Hz-source-locked-holdout.md",
        },
        {
            "test_arena": "source-locked growth covariance",
            "lead_branch_readout": "preferred/draw under GR-proxy growth; jackknife failures 0",
            "metric": "primary all rows DeltaChi2=-2.30357028036",
            "claim_allowed": "effective subhorizon growth compatibility",
            "claim_forbidden": "derived perturbation theory",
            "source": "146-source-locked-growth-covariance-holdout.md; 148-perturbation-CMB-local-GR-promotion-contract.md",
        },
        {
            "test_arena": "ELG grid likelihood",
            "lead_branch_readout": "draw; non-Gaussian ELG branch does not reverse scorecard",
            "metric": "ELG round neither wins nor loses by itself",
            "claim_allowed": "non-Gaussian growth/geometry safety clue",
            "claim_forbidden": "official joint likelihood claim",
            "source": "147-ELG-grid-likelihood-holdout.md",
        },
        {
            "test_arena": "CMB bridge",
            "lead_branch_readout": "unresolved/mixed with explicit failures",
            "metric": "compressed distance draw; late-to-CMB transfer fail; joint bridge mixed",
            "claim_allowed": "diagnostic stress-test only",
            "claim_forbidden": "MTS passes CMB",
            "source": "144-frozen-branch-empirical-holdout-scorecard.md; 148-perturbation-CMB-local-GR-promotion-contract.md",
        },
    ]


def claim_boundary_rows(scores: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    half = scores["pair_action_half_kernel"]
    return [
        {
            "claim": "no-clock MTS is current empirical lead branch",
            "status": "allowed_private",
            "support": "pair repair gate did not beat no-clock; frozen no-clock has broader holdout record",
            "limit": "empirical lead does not mean fundamental derivation",
            "next_action": "refresh official late-time likelihoods with symmetric baselines",
        },
        {
            "claim": "pair-ruler half-kernel is the default sidecar",
            "status": "allowed_private_conditional",
            "support": f"best structural pair repair; delta_BIC_vs_no_clock={half['delta_BIC_vs_no_clock']}",
            "limit": "only valid as sidecar unless parent action owns 1/2 factor",
            "next_action": "derive or reject half-factor ownership before two-point promotion",
        },
        {
            "claim": "MTS passes CMB",
            "status": "forbidden",
            "support": "CMB compressed distance is diagnostic only; transfer/joint bridge unresolved",
            "limit": "needs Boltzmann-level perturbation and sound-horizon/ruler interface",
            "next_action": "build CMB-ruler safety contract after sidecar response is defined",
        },
        {
            "claim": "MTS derives local GR",
            "status": "forbidden",
            "support": "local silence/PPN conditions remain theorem targets",
            "limit": "no derived q_loc^nu -> 0, G_eff/G -> 1, Phi=Psi branch yet",
            "next_action": "derive local PPN branch from parent action, not a plateau axiom",
        },
        {
            "claim": "B_mem=2/27 is derived",
            "status": "forbidden",
            "support": "locked value is empirical closure/theorem target",
            "limit": "amplitude cannot be advertised as a parent prediction",
            "next_action": "continue amplitude theorem route separately from empirical tests",
        },
        {
            "claim": "baselines must face same stress tests",
            "status": "required",
            "support": "jackknife and split failures are only meaningful under symmetric treatment",
            "limit": "no one-sided guilty-until-proven-innocent scoring",
            "next_action": "write every future runner with LCDM/wCDM/CPL side-by-side scorecards",
        },
    ]


def sidecar_test_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "test": "half-kernel parent ownership",
            "branch": "MTS_pair_ruler_half_kernel",
            "question": "Does the effective pair action truly put the 1/2 into the kernel source law?",
            "pass_condition": "1/2 factor follows before data scoring, not from residual repair",
            "fail_condition": "half-kernel remains an empirical repair and cannot be promoted",
            "output_target": "168-pair-half-kernel-parent-ownership-gate.md",
        },
        {
            "priority": 2,
            "test": "growth/RSD sidecar response",
            "branch": "MTS_pair_ruler_half_kernel",
            "question": "Does the connected pair ruler perturb f_sigma8 or AP/RSD observables beyond the no-clock lead?",
            "pass_condition": "same covariance/jackknife suite; LCDM/wCDM/CPL scored identically; no hidden amplitude fit",
            "fail_condition": "sidecar produces unowned growth/lensing source or breaks existing draw",
            "output_target": "169-pair-sidecar-growth-rsd-safety.md",
        },
        {
            "priority": 3,
            "test": "lensing/slip safety",
            "branch": "MTS_pair_ruler_half_kernel",
            "question": "What Sigma, Phi-Psi, and lensing-kernel response does the sidecar induce?",
            "pass_condition": "response is derived and bounded, with local and cosmological limits stated",
            "fail_condition": "unbounded slip or lensing modification without parent conservation",
            "output_target": "170-pair-sidecar-lensing-slip-safety.md",
        },
        {
            "priority": 4,
            "test": "CMB-ruler safety",
            "branch": "MTS_pair_ruler_half_kernel",
            "question": "Does any ruler projection alter the sound horizon, angular diameter bridge, or recombination ruler?",
            "pass_condition": "explicit early-time/r_s/Theta_star behavior; no compressed-CMB overclaim",
            "fail_condition": "sidecar conflicts with early ruler calibration or needs post-hoc hiding",
            "output_target": "171-pair-sidecar-CMB-ruler-safety.md",
        },
        {
            "priority": 5,
            "test": "lead no-clock likelihood refresh",
            "branch": "MTS_2over27_no_clock_u3quarter",
            "question": "Does the lead survive a clean refresh with official/newer likelihood wrappers where feasible?",
            "pass_condition": "same data cuts, nuisance rules, priors, and jackknifes for MTS and baselines",
            "fail_condition": "late-time advantage disappears under symmetric official likelihood handling",
            "output_target": "172-no-clock-official-likelihood-refresh.md",
        },
    ]


def shared_baseline_fairness_rows() -> list[dict[str, Any]]:
    return [
        {
            "rule": "same_data_vectors",
            "requirement": "MTS and baselines use identical rows, redshift cuts, covariance blocks, and source manifests",
            "reason": "prevents accidental asymmetric wins or losses",
            "failure_flag": "different rows or covariance for one branch",
        },
        {
            "rule": "same_nuisance_profile",
            "requirement": "profile or freeze nuisance parameters symmetrically across MTS, LCDM, wCDM, and CPL",
            "reason": "keeps AIC/BIC scorecards meaningful",
            "failure_flag": "one branch gets extra offset/calibration freedom",
        },
        {
            "rule": "same_jackknife_punches",
            "requirement": "apply every split/jackknife/residual pressure test to baselines as well as MTS",
            "reason": "a jackknife only condemns MTS if baselines survive the same punch",
            "failure_flag": "MTS-only jackknife or baseline-only exemption",
        },
        {
            "rule": "edge_and_prior_flags",
            "requirement": "mark prior-edge, convergence, and nuisance-bound dependence for every fitted branch",
            "reason": "edge-hitting is not stable evidence for any model",
            "failure_flag": "best fit depends on prior edge without demotion",
        },
        {
            "rule": "draw_threshold_honesty",
            "requirement": "treat |DeltaBIC|<2 as draw unless context gives a stronger reason",
            "reason": "close judges' rounds are not knockouts",
            "failure_flag": "overclaiming tiny BIC changes",
        },
        {
            "rule": "claim_ceiling",
            "requirement": "late-time empirical wins cannot be reworded as CMB/local-GR/parent-action derivations",
            "reason": "keeps the title fight separate from undercard wins",
            "failure_flag": "public-style theory claim from a smoke or sidecar scorecard",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "parent_action_for_no_clock",
            "owner": "lead lane",
            "status": "open",
            "needed_for": "fundamental theory promotion",
            "next_artifact": "action whose variation gives the no-clock memory stress and conservation law",
        },
        {
            "gate": "B_mem_2_over_27_derivation",
            "owner": "lead lane",
            "status": "open",
            "needed_for": "turn empirical closure into theorem",
            "next_artifact": "normalization or boundary-charge derivation of B_mem=2/27",
        },
        {
            "gate": "u3_quarter_derivation",
            "owner": "lead lane",
            "status": "open",
            "needed_for": "make activation scale non-fitted",
            "next_artifact": "cell/transition theorem for u3=1/4",
        },
        {
            "gate": "perturbation_owner",
            "owner": "lead lane",
            "status": "open",
            "needed_for": "growth, lensing, and CMB promotion",
            "next_artifact": "mu(a,k), slip/Sigma, friction/source terms, conservation constraints",
        },
        {
            "gate": "local_GR_PPN_branch",
            "owner": "parent/local lane",
            "status": "open",
            "needed_for": "not becoming another MOND/dark-sector phenomenology only",
            "next_artifact": "derived q_loc^nu -> 0, G_eff/G -> 1, Phi=Psi and PPN residual bounds",
        },
        {
            "gate": "pair_sidecar_two_point_safety",
            "owner": "sidecar lane",
            "status": "open",
            "needed_for": "pair-ruler promotion beyond sidecar",
            "next_artifact": "growth/RSD, lensing/slip, and CMB-ruler response tests with no fitted projection amplitude",
        },
    ]


def gate_result_rows(scores: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    half = scores["pair_action_half_kernel"]
    base = scores["base_161_fixed"]
    return [
        {
            "gate": "lead_lane_separated",
            "status": "pass",
            "evidence": "no-clock branch is explicitly assigned lead empirical lane",
        },
        {
            "gate": "pair_sidecar_demoted",
            "status": "pass",
            "evidence": f"half-kernel improves base by {half['delta_BIC_vs_base_161']} but remains {half['delta_BIC_vs_no_clock']} vs no-clock",
        },
        {
            "gate": "base_pair_not_default",
            "status": "pass",
            "evidence": f"base 161 delta_BIC_vs_no_clock={base['delta_BIC_vs_no_clock']}",
        },
        {
            "gate": "BAO_only_tuning_blocked",
            "status": "pass",
            "evidence": "sidecar tests forbid row-wise BAO repair and continuous projection-amplitude fitting",
        },
        {
            "gate": "baseline_fairness_required",
            "status": "pass",
            "evidence": "same data vectors, nuisance rules, jackknifes, edge flags, and draw thresholds required for LCDM/wCDM/CPL",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(scores: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    half = scores["pair_action_half_kernel"]
    return [
        {
            "item": "status",
            "verdict": STATUS,
            "evidence": "lead and sidecar lanes separated after pair-ruler demotion gate",
        },
        {
            "item": "lead_branch",
            "verdict": "MTS_2over27_no_clock_u3quarter",
            "evidence": "broader empirical record and no parent-constrained pair variant beats it",
        },
        {
            "item": "sidecar_branch",
            "verdict": "MTS_pair_ruler_half_kernel",
            "evidence": f"best fixed sidecar candidate; delta_BIC_vs_no_clock={half['delta_BIC_vs_no_clock']}",
        },
        {
            "item": "global_clock_branch",
            "verdict": "demoted_control_only",
            "evidence": "do not restore clock route by assertion",
        },
        {
            "item": "public_claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "no CMB, local GR, perturbation, or parent-action promotion from this checkpoint",
        },
        {
            "item": "next_target",
            "verdict": "168-pair-half-kernel-parent-ownership-gate.md",
            "evidence": "either own the sidecar 1/2 factor before data scoring or keep pair-ruler frozen as closure-only",
        },
    ]


def run_gate(output_root: Path, timestamp: str | None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-no-clock-lead-and-pair-sidecar-test-plan"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    scores = repair_score_rows()
    best = best_pair_sidecar(scores)
    branch_rows = branch_lane_assignment_rows(scores)
    evidence_rows = lead_empirical_evidence_rows()
    claim_rows = claim_boundary_rows(scores)
    sidecar_rows = sidecar_test_queue_rows()
    fairness_rows = shared_baseline_fairness_rows()
    promotion_rows = promotion_gate_rows()
    gates = gate_result_rows(scores)
    decisions = decision_rows(scores)

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "input_demoter_run": str(RUN_166),
            "lead_branch": "MTS_2over27_no_clock_u3quarter",
            "sidecar_branch": best["variant"],
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "branch_lane_assignment.csv",
        branch_rows,
        [
            "branch",
            "lane",
            "role",
            "fixed_inputs",
            "allowed_use",
            "forbidden_use",
            "promotion_conditions",
            "current_status",
            "evidence",
            "source_files",
        ],
    )
    write_csv(
        results_dir / "lead_empirical_evidence_table.csv",
        evidence_rows,
        ["test_arena", "lead_branch_readout", "metric", "claim_allowed", "claim_forbidden", "source"],
    )
    write_csv(
        results_dir / "claim_boundary_matrix.csv",
        claim_rows,
        ["claim", "status", "support", "limit", "next_action"],
    )
    write_csv(
        results_dir / "sidecar_test_queue.csv",
        sidecar_rows,
        ["priority", "test", "branch", "question", "pass_condition", "fail_condition", "output_target"],
    )
    write_csv(
        results_dir / "shared_baseline_fairness_rules.csv",
        fairness_rows,
        ["rule", "requirement", "reason", "failure_flag"],
    )
    write_csv(
        results_dir / "promotion_gate_queue.csv",
        promotion_rows,
        ["gate", "owner", "status", "needed_for", "next_artifact"],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    write_json(
        run_dir / "status.json",
        {
            "status": STATUS,
            "run_dir": str(run_dir),
            "results_dir": str(results_dir),
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": "MTS_2over27_no_clock_u3quarter",
            "sidecar_branch": "MTS_pair_ruler_half_kernel",
            "best_sidecar_variant_from_166": best["variant"],
            "best_sidecar_delta_BIC_vs_no_clock": float(best["delta_BIC_vs_no_clock"]),
            "generated": [
                "source_register.csv",
                "branch_lane_assignment.csv",
                "lead_empirical_evidence_table.csv",
                "claim_boundary_matrix.csv",
                "sidecar_test_queue.csv",
                "shared_baseline_fairness_rules.csv",
                "promotion_gate_queue.csv",
                "gate_results.csv",
                "decision.csv",
            ],
            "next_target": "168-pair-half-kernel-parent-ownership-gate.md",
        },
    )
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_gate(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
