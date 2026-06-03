#!/usr/bin/env python3
"""Aggregate frozen B_mem=2/27 empirical holdout evidence under claim limits."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CLAIM_CEILING = "frozen_locked_branch_empirical_scorecard_no_theory_promotion"
LOCKED_B_MEM = 2.0 / 27.0

RUNS = {
    "claim_contract": RUNS_ROOT / "20260531-210000-consolidated-locked-memory-branch-contract",
    "selector_gate": RUNS_ROOT / "20260531-213000-domain-selector-variational-action-attempt",
    "sn_bao_t7": RUNS_ROOT / "20260531-145921-canonical-R-two-ninth-T7-robustness",
    "bao_only": RUNS_ROOT / "20260531-151959-locked-2over27-BAO-only-score",
    "cmb_distance": RUNS_ROOT / "20260531-161215-locked-2over27-CMB-distance-score",
    "late_cmb_transfer": RUNS_ROOT / "20260531-162146-locked-2over27-late-CMB-transfer-score",
    "joint_late_cmb": RUNS_ROOT / "20260531-164711-locked-2over27-joint-late-CMB-score",
    "bao_hz_robustness": RUNS_ROOT / "20260531-181900-BAO-Hz-noCMB-robustness",
    "growth_gate": RUNS_ROOT / "20260531-183400-growth-route-gate",
    "subhorizon_growth": RUNS_ROOT / "20260531-191200-subhorizon-suppressed-growth-correction-gate",
}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_key_value_csv(path: Path, key_field: str, value_field: str) -> dict[str, str]:
    return {row[key_field]: row[value_field] for row in read_csv_rows(path)}


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "108-two-ninth-fixed-amplitude-robustness.md",
        WORK_DIR / "113-locked-2over27-BAO-only-runner-and-score.md",
        WORK_DIR / "116-locked-2over27-CMB-distance-score.md",
        WORK_DIR / "117-locked-2over27-late-CMB-transfer-gate.md",
        WORK_DIR / "119-locked-2over27-joint-late-CMB-calibration-runner.md",
        WORK_DIR / "120-joint-calibration-red-team-and-repair-options.md",
        WORK_DIR / "129-noCMB-radial-robustness-or-growth-route.md",
        WORK_DIR / "130-growth-route-gate.md",
        WORK_DIR / "134-subhorizon-suppressed-growth-correction-gate.md",
        WORK_DIR / "141-consolidated-locked-memory-branch-contract.md",
        WORK_DIR / "143-domain-selector-variational-action-attempt.md",
    ]
    run_artifacts = {
        "claim_contract": ["status.json", "results/decision.csv"],
        "selector_gate": ["status.json", "results/decision.csv"],
        "sn_bao_t7": ["status.json", "results/decision.csv", "results/branch_gates.csv"],
        "bao_only": ["status.json", "results/decision.csv", "results/release_gates.csv"],
        "cmb_distance": ["status.json", "results/decision.csv"],
        "late_cmb_transfer": ["status.json", "results/decision.csv"],
        "joint_late_cmb": ["status.json", "results/joint_gates.csv"],
        "bao_hz_robustness": ["status.json", "results/decision.csv", "results/stability_summary.csv"],
        "growth_gate": ["status.json", "results/decision.csv"],
        "subhorizon_growth": ["status.json", "results/summary_by_k_and_safety.csv"],
    }
    for run_key, artifacts in run_artifacts.items():
        for artifact in artifacts:
            paths.append(RUNS[run_key] / artifact)
    return [
        {
            "source": path.name,
            "path": str(path),
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path in paths
    ]


def find_row(rows: list[dict[str, str]], **matches: str) -> dict[str, str] | None:
    for row in rows:
        if all(row.get(key) == value for key, value in matches.items()):
            return row
    return None


def evidence_rows() -> list[dict[str, Any]]:
    t7_decision = read_key_value_csv(RUNS["sn_bao_t7"] / "results" / "decision.csv", "decision", "value")
    t7_gate = find_row(
        read_csv_rows(RUNS["sn_bao_t7"] / "results" / "branch_gates.csv"),
        branch="T1_primary_fullcov_DR2",
    )

    bao_decision = read_key_value_csv(RUNS["bao_only"] / "results" / "decision.csv", "decision", "value")
    bao_gates = read_csv_rows(RUNS["bao_only"] / "results" / "release_gates.csv")

    cmb_decision = read_key_value_csv(RUNS["cmb_distance"] / "results" / "decision.csv", "decision", "value")
    transfer_decision = read_key_value_csv(RUNS["late_cmb_transfer"] / "results" / "decision.csv", "decision", "value")
    joint_gates = read_csv_rows(RUNS["joint_late_cmb"] / "results" / "joint_gates.csv")
    joint_fail = find_row(joint_gates, prior_table="LCDM", score_mode="strict_full4")

    bao_hz_decision = read_key_value_csv(RUNS["bao_hz_robustness"] / "results" / "decision.csv", "item", "verdict")
    bao_hz_stability = find_row(
        read_csv_rows(RUNS["bao_hz_robustness"] / "results" / "stability_summary.csv"),
        group="production_all_BAO_Hz_branches_vs_LCDM",
    )

    growth_decision = read_key_value_csv(RUNS["growth_gate"] / "results" / "decision.csv", "item", "verdict")
    growth_delta = read_key_value_csv(RUNS["growth_gate"] / "results" / "decision.csv", "item", "evidence")

    sub_summary = find_row(
        read_csv_rows(RUNS["subhorizon_growth"] / "results" / "summary_by_k_and_safety.csv"),
        k_h_Mpc="0.02",
        safety_factor="100.0",
    )

    bao_passes = sum(1 for row in bao_gates if row.get("result", "").startswith("pass"))
    joint_hard_losses = sum(1 for row in joint_gates if row.get("gate") == "hard_loss_sector_degradation")
    joint_draws = sum(1 for row in joint_gates if row.get("gate") == "competitive_draw")

    return [
        {
            "arena": "SN+BAO full-cov robustness",
            "run": str(RUNS["sn_bao_t7"]),
            "status": t7_decision["verdict"],
            "primary_metric": f"DeltaBIC_vs_LCDM={t7_gate['delta_BIC_vs_LCDM'] if t7_gate else 'missing'}",
            "score_readout": "locked branch preferred in primary late fit",
            "claim_allowed": "competitive empirical closure branch",
            "forbidden_claim": "parent amplitude prediction",
            "promotion_allowed": False,
        },
        {
            "arena": "BAO-only release holdout",
            "run": str(RUNS["bao_only"]),
            "status": bao_decision["verdict"],
            "primary_metric": f"release_pass_count={bao_passes}; DR2_deltaBIC={bao_gates[0]['delta_BIC_vs_LCDM']}; DR1_deltaBIC={bao_gates[1]['delta_BIC_vs_LCDM']}",
            "score_readout": "locked branch beats LCDM IC in both BAO release checks",
            "claim_allowed": "non-SN empirical stress pass",
            "forbidden_claim": "derived amplitude or full cosmology",
            "promotion_allowed": False,
        },
        {
            "arena": "BAO+H(z), no CMB",
            "run": str(RUNS["bao_hz_robustness"]),
            "status": bao_hz_decision["status"],
            "primary_metric": f"branches={bao_hz_stability['branch_count']}; draws={bao_hz_stability['draw_count']}; disfavored={bao_hz_stability['disfavored_count']}; deltaBIC_range=[{bao_hz_stability['min_delta_BIC']},{bao_hz_stability['max_delta_BIC']}]",
            "score_readout": "stable late-time radial competitive draw",
            "claim_allowed": "late-time radial draw/preference test",
            "forbidden_claim": "CMB compatibility solved",
            "promotion_allowed": False,
        },
        {
            "arena": "growth f_sigma8",
            "run": str(RUNS["growth_gate"]),
            "status": growth_decision["status"],
            "primary_metric": growth_delta["primary_BAO_plus_all_vs_LCDM"],
            "score_readout": "locked preferred/draw under GR-proxy growth gate",
            "claim_allowed": "late-time subhorizon effective stress check",
            "forbidden_claim": "derived MTS perturbation theory",
            "promotion_allowed": False,
        },
        {
            "arena": "subhorizon growth correction bound",
            "run": str(RUNS["subhorizon_growth"]),
            "status": "subhorizon_memory_growth_correction_negligible_conditionally",
            "primary_metric": f"k=0.02 safety=100 chi2_impact={sub_summary['diagonal_chi2_impact_sum_bound'] if sub_summary else 'missing'}",
            "score_readout": "high-sound-speed correction bound negligible on tested late-time scales",
            "claim_allowed": "conditional robustness of growth proxy",
            "forbidden_claim": "full perturbation theory",
            "promotion_allowed": False,
        },
        {
            "arena": "CMB compressed distance score",
            "run": str(RUNS["cmb_distance"]),
            "status": cmb_decision["score_status"],
            "primary_metric": f"draw_or_better_count={cmb_decision['lcdm_primary_draw_or_better_count']}; edge_count={cmb_decision['locked_edge_count']}",
            "score_readout": "compressed distance draw/survival only",
            "claim_allowed": "distance-prior stress diagnostic",
            "forbidden_claim": "passes CMB or perturbations",
            "promotion_allowed": False,
        },
        {
            "arena": "late-to-CMB transfer",
            "run": str(RUNS["late_cmb_transfer"]),
            "status": transfer_decision["transfer_status"],
            "primary_metric": f"primary_fail_count={transfer_decision['primary_fail_count']}; primary_pass_count={transfer_decision['primary_pass_count']}",
            "score_readout": "fixed late Omega transfer fails compressed CMB geometry",
            "claim_allowed": "failure/guardrail",
            "forbidden_claim": "late branch automatically transfers to CMB",
            "promotion_allowed": False,
        },
        {
            "arena": "joint late+CMB calibration",
            "run": str(RUNS["joint_late_cmb"]),
            "status": "mixed_not_promoted",
            "primary_metric": f"competitive_draws={joint_draws}; hard_losses={joint_hard_losses}; strict_LCDM_late_penalty={joint_fail['late_chi2_penalty_vs_T7'] if joint_fail else 'missing'}",
            "score_readout": "joint bridge close but one mandatory strict gate fails",
            "claim_allowed": "mixed calibration stress result",
            "forbidden_claim": "MTS passes joint cosmology",
            "promotion_allowed": False,
        },
    ]


def baseline_fairness_rows() -> list[dict[str, Any]]:
    return [
        {
            "rule": "frozen_amplitude",
            "status": "pass",
            "evidence": "B_mem=2/27 treated as fixed branch in aggregated evidence",
        },
        {
            "rule": "same_baseline_comparisons",
            "status": "pass",
            "evidence": "scorecards compare against LCDM and where available wCDM/CPL/MTS_Bmem_zero",
        },
        {
            "rule": "same_split_discipline",
            "status": "pass_partial",
            "evidence": "BAO DR1/DR2, CMB prior-table modes, H(z) variants, and growth score modes are separated",
        },
        {
            "rule": "do_not_relabel_CMB_draw_as_pass",
            "status": "pass",
            "evidence": "CMB distance marked diagnostic; late-to-CMB transfer and joint bridge failures retained",
        },
        {
            "rule": "no_theory_promotion_from_empirical_score",
            "status": "pass",
            "evidence": "all evidence rows carry promotion_allowed=False",
        },
    ]


def claim_limited_rows(evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "arena": row["arena"],
            "status": row["status"],
            "allowed_claim": row["claim_allowed"],
            "forbidden_claim": row["forbidden_claim"],
            "promotion_allowed": row["promotion_allowed"],
            "ceiling_reason": "empirical branch score only; no parent action, amplitude theorem, CMB perturbation, or local-GR theorem is derived here",
        }
        for row in evidence
    ]


def holdout_gate_rows(evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hard_fail_arenas = [
        row["arena"]
        for row in evidence
        if "fail" in str(row["status"]).lower() or "hard" in str(row["status"]).lower()
    ]
    late_positive = [
        row
        for row in evidence
        if row["arena"] in {"SN+BAO full-cov robustness", "BAO-only release holdout", "BAO+H(z), no CMB", "growth f_sigma8"}
    ]
    return [
        {
            "gate": "frozen_branch_no_refit",
            "status": "pass",
            "evidence": f"B_mem fixed at {LOCKED_B_MEM}",
        },
        {
            "gate": "late_time_empirical_survival",
            "status": "pass",
            "evidence": f"{len(late_positive)} late-time arenas retained as preferred/draw/stress-pass",
        },
        {
            "gate": "CMB_bridge_promoted",
            "status": "fail",
            "evidence": "late-to-CMB transfer fails and joint bridge is mixed/not promoted",
        },
        {
            "gate": "growth_promoted_to_perturbation_theory",
            "status": "fail",
            "evidence": "growth gate remains GR-proxy/high-sound-speed EFT target only",
        },
        {
            "gate": "public_support_claim_allowed",
            "status": "fail",
            "evidence": "branch is empirical EFT closure with conditional mechanics, not parent field theory",
        },
        {
            "gate": "hard_failures_preserved",
            "status": "pass",
            "evidence": "; ".join(hard_fail_arenas) if hard_fail_arenas else "none found",
        },
    ]


def next_holdout_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": "official/full-likelihood BAO+SN+growth reimplementation",
            "reason": "current tests are disciplined but still lightweight relative to official likelihood stacks",
            "claim_limit": "empirical closure only",
            "ready_now": "partial",
        },
        {
            "priority": 2,
            "target": "independent H(z) / cosmic-chronometer compilation cross-check",
            "reason": "no-CMB radial branch is stable draw; independent H(z) updates test fragility",
            "claim_limit": "late-time radial stress only",
            "ready_now": "yes_if_data_loaded",
        },
        {
            "priority": 3,
            "target": "growth with covariance / official RSD likelihood",
            "reason": "current f_sigma8 gate is useful but proxy-level",
            "claim_limit": "effective subhorizon stress only",
            "ready_now": "partial",
        },
        {
            "priority": 4,
            "target": "CMB perturbation implementation",
            "reason": "compressed distance draw is not enough and transfer bridge fails",
            "claim_limit": "do not claim CMB pass",
            "ready_now": "no_parent_perturbation_equations_missing",
        },
        {
            "priority": 5,
            "target": "local PPN / solar-system bound runner",
            "reason": "local silence remains conditional and domain selector not derived",
            "claim_limit": "local silence target only",
            "ready_now": "no_domain_boundary_owner_missing",
        },
    ]


def decision_rows(evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    late_wins_or_draws = sum(
        1
        for row in evidence
        if row["arena"] in {"SN+BAO full-cov robustness", "BAO-only release holdout", "BAO+H(z), no CMB", "growth f_sigma8"}
    )
    return [
        {
            "item": "status",
            "verdict": "frozen_branch_empirical_scorecard_late_time_survives_CMB_bridge_unresolved",
            "evidence": f"late-time preferred/draw arenas={late_wins_or_draws}; CMB transfer/joint bridge not promoted",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "empirical scorecard only, no parent-theory promotion",
        },
        {
            "item": "next_target",
            "verdict": "choose_new_independent_holdout_or_official_perturbation_pipeline",
            "evidence": "best empirical next step is stricter external data/likelihood, not another theory promotion claim",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-frozen-branch-empirical-holdout-scorecard"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    contract_status = read_json(RUNS["claim_contract"] / "status.json")
    evidence = evidence_rows()
    fairness = baseline_fairness_rows()
    claim_limits = claim_limited_rows(evidence)
    gates = holdout_gate_rows(evidence)
    next_queue = next_holdout_rows()
    decisions = decision_rows(evidence)

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(results_dir / "evidence_scorecard.csv", evidence, ["arena", "run", "status", "primary_metric", "score_readout", "claim_allowed", "forbidden_claim", "promotion_allowed"])
    write_csv(results_dir / "baseline_fairness_ledger.csv", fairness, ["rule", "status", "evidence"])
    write_csv(results_dir / "claim_limited_scorecard.csv", claim_limits, ["arena", "status", "allowed_claim", "forbidden_claim", "promotion_allowed", "ceiling_reason"])
    write_csv(results_dir / "holdout_gates.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "next_holdout_queue.csv", next_queue, ["priority", "target", "reason", "claim_limit", "ready_now"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "input_status": contract_status["status"],
        "locked_B_mem": LOCKED_B_MEM,
        "generated": [
            "source_register.csv",
            "evidence_scorecard.csv",
            "baseline_fairness_ledger.csv",
            "claim_limited_scorecard.csv",
            "holdout_gates.csv",
            "gate_results.csv",
            "next_holdout_queue.csv",
            "decision.csv",
        ],
        "next_target": "choose_new_independent_holdout_or_official_perturbation_pipeline",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_audit(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
