#!/usr/bin/env python3
"""Consolidate canonical_R_closure cosmology robustness checks T1-T6."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RUNS_ROOT = POST_CHECKPOINT / "runs"

CHECKPOINTS = {
    "T1": POST_CHECKPOINT / "100-canonical-R-T1-primary-fullcov-scorecard.md",
    "T2": POST_CHECKPOINT / "101-canonical-R-T2-ablation-scorecard.md",
    "T3": POST_CHECKPOINT / "102-canonical-R-T3-diagonal-covariance-sensitivity.md",
    "T4": POST_CHECKPOINT / "103-canonical-R-T4-small-sample-reproduction.md",
    "T5": POST_CHECKPOINT / "104-canonical-R-T5-SH0ES-pressure-branch.md",
    "T6": POST_CHECKPOINT / "105-canonical-R-T6-BAO-release-sensitivity.md",
}

LEDGERS = {
    "T1": RUNS_ROOT / "20260531-141359-canonical-R-T1-scorecard",
    "T2": RUNS_ROOT / "20260531-141851-canonical-R-T2-ablation-scorecard",
    "T3": RUNS_ROOT / "20260531-142400-canonical-R-T3-covariance-scorecard",
    "T4": RUNS_ROOT / "20260531-142827-canonical-R-T4-small-sample-scorecard",
    "T5": RUNS_ROOT / "20260531-143518-canonical-R-T5-SH0ES-pressure-scorecard",
    "T6": RUNS_ROOT / "20260531-144136-canonical-R-T6-BAO-release-scorecard",
}

SCORE_RUNS = {
    "T1_primary_fullcov_DR2": RUNS_ROOT / "20260531-141154-cosmo-SN-BAO-short-smoke",
    "T2_fullcov_DR2_ablations": RUNS_ROOT / "20260531-141635-cosmo-SN-BAO-short-smoke",
    "T3_diagonal_DR2": RUNS_ROOT / "20260531-142133-cosmo-SN-BAO-short-smoke",
    "T4_small_fullcov_DR2": RUNS_ROOT / "20260531-142622-cosmo-SN-BAO-short-smoke",
    "T5_SH0ES_pressure": RUNS_ROOT / "20260531-143143-cosmo-SN-BAO-short-smoke",
    "T5_matched_control": RUNS_ROOT / "20260531-143247-cosmo-SN-BAO-short-smoke",
    "T6_small_fullcov_DR1": RUNS_ROOT / "20260531-143908-cosmo-SN-BAO-short-smoke",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def decision_value(run_dir: Path, key: str) -> str:
    rows = read_csv(run_dir / "results" / "decision.csv")
    for row in rows:
        if row["decision"] == key:
            return row["value"]
    return ""


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, path in CHECKPOINTS.items():
        rows.append({"label": label, "path": str(path), "exists": path.exists(), "kind": "checkpoint"})
    for label, path in LEDGERS.items():
        rows.append({"label": label, "path": str(path), "exists": path.exists(), "kind": "ledger_run"})
    for label, path in SCORE_RUNS.items():
        rows.append({"label": label, "path": str(path), "exists": path.exists(), "kind": "score_run"})
    return rows


def robustness_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "T1_primary_fullcov",
            "verdict": decision_value(LEDGERS["T1"], "verdict"),
            "scorecard_role": "primary_title_card",
            "positive_read": "edge-free full-sample full-covariance DR2 branch; beats wCDM narrowly and CPL by AIC/BIC",
            "warning": "loses weakly to LCDM on BIC; amplitude still fitted",
            "claim_allowed": "empirical closure contender",
        },
        {
            "test": "T2_fixed_shape_ablation",
            "verdict": decision_value(LEDGERS["T2"], "verdict"),
            "scorecard_role": "shape_discipline_test",
            "positive_read": "free p/u3 improve raw chi2 only mildly and lose AIC/BIC against fixed branch",
            "warning": "p/u3 are still not parent-action derived",
            "claim_allowed": "fixed closure shape survives first ablation",
        },
        {
            "test": "T3_diagonal_covariance",
            "verdict": decision_value(LEDGERS["T3"], "verdict"),
            "scorecard_role": "covariance_sensitivity_diagnostic",
            "positive_read": "diagonal covariance preserves or strengthens relative pattern",
            "warning": "diagonal covariance is weaker than full covariance; B_mem shifts about 32%",
            "claim_allowed": "not a full-covariance artifact",
        },
        {
            "test": "T4_small_sample",
            "verdict": decision_value(LEDGERS["T4"], "verdict"),
            "scorecard_role": "small_sample_pipeline_warning",
            "positive_read": "fixed branch stays edge-free and preserves broad pattern",
            "warning": "CPL and fitted-u3 edge-hit; small branch is diagnostic only",
            "claim_allowed": "older small-smoke instability reproduced and quarantined",
        },
        {
            "test": "T5_SH0ES_pressure",
            "verdict": decision_value(LEDGERS["T5"], "verdict"),
            "scorecard_role": "local_H0_pressure_stress_test",
            "positive_read": "fixed branch stays edge-free; SH0ES observable barely changes relative scorecard",
            "warning": "CPL edge-hit persists; stress branch is not support",
            "claim_allowed": "SH0ES pressure is neutral, not special evidence",
        },
        {
            "test": "T6_BAO_release",
            "verdict": decision_value(LEDGERS["T6"], "verdict"),
            "scorecard_role": "anti_cherrypick_release_test",
            "positive_read": "DR1 preserves wCDM win and CPL parsimony round; fixed branch edge-free",
            "warning": "DR1 weakens LCDM/AIC and memory-vs-zero AIC; do not cherry-pick DR2",
            "claim_allowed": "BAO-release warning, not reversal",
        },
    ]


def primary_score_rows() -> list[dict[str, Any]]:
    t1_judge = read_csv(LEDGERS["T1"] / "results" / "judge_card.csv")
    t2_ablation = read_csv(LEDGERS["T2"] / "results" / "ablation_vs_fixed.csv")
    t3_amplitude = read_csv(LEDGERS["T3"] / "results" / "amplitude_sensitivity.csv")
    t6_memory = read_csv(LEDGERS["T6"] / "results" / "memory_signal_by_release.csv")
    rows: list[dict[str, Any]] = []
    for row in t1_judge:
        rows.append(
            {
                "topic": f"T1_vs_{row['reference']}",
                "delta_chi2": row["delta_chi2"],
                "delta_AIC": row["delta_AIC"],
                "delta_BIC": row["delta_BIC"],
                "readout": row["round_label"],
            }
        )
    for row in t2_ablation:
        rows.append(
            {
                "topic": f"T2_{row['ablation']}_vs_fixed",
                "delta_chi2": row["delta_chi2"],
                "delta_AIC": row["delta_AIC"],
                "delta_BIC": row["delta_BIC"],
                "readout": row["verdict"],
            }
        )
    for row in t3_amplitude:
        if row["quantity"] == "B_mem":
            rows.append(
                {
                    "topic": "T3_Bmem_full_to_diagonal",
                    "delta_chi2": "",
                    "delta_AIC": "",
                    "delta_BIC": "",
                    "readout": f"relative_shift={row['relative_shift']}; {row['verdict']}",
                }
            )
    for row in t6_memory:
        rows.append(
            {
                "topic": f"T6_memory_signal_{row['release']}",
                "delta_chi2": row["fixed_minus_zero_chi2"],
                "delta_AIC": row["fixed_minus_zero_AIC"],
                "delta_BIC": row["fixed_minus_zero_BIC"],
                "readout": "fixed canonical minus zero-memory control",
            }
        )
    return rows


def instability_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources = [
        ("T4_small_sample", LEDGERS["T4"] / "results" / "edge_flag_reproduction.csv"),
        ("T5_SH0ES_pressure", LEDGERS["T5"] / "results" / "edge_flag_comparison.csv"),
        ("T6_BAO_release", LEDGERS["T6"] / "results" / "edge_flag_release_comparison.csv"),
    ]
    for source, path in sources:
        for row in read_csv(path):
            model = row.get("model", "")
            parameter = row.get("parameter", "")
            if not model and not parameter:
                continue
            rows.append(
                {
                    "source": source,
                    "branch_or_release": row.get("branch", row.get("release", "")),
                    "model": model,
                    "parameter": parameter,
                    "best_fit": row.get("best_fit", ""),
                    "interpretation": row.get("interpretation", ""),
                }
            )
    return rows


def theory_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "claim_ceiling",
            "current_status": "empirical_closure_scorecard_only",
            "must_derive_or_verify": "Do not describe canonical_R_closure as a parent-action prediction.",
            "priority": 0,
        },
        {
            "gate": "B_mem_amplitude_owner",
            "current_status": "fitted amplitude; useful signal but not predicted",
            "must_derive_or_verify": "Derive B_mem or equivalent DeltaR endpoint amplitude from the parent action before amplitude claims.",
            "priority": 1,
        },
        {
            "gate": "canonical_R_normalization",
            "current_status": "a_F=1 and R unit scale are closure choices",
            "must_derive_or_verify": "Fix the R normalization by field metric, boundary charge, and trace/Ward identity rather than convention.",
            "priority": 2,
        },
        {
            "gate": "p_and_u3_ownership",
            "current_status": "fixed p=3 and u3=1/4 survive ablations but are not derived",
            "must_derive_or_verify": "Recover p=3 and u3=1/4 from the local-to-FLRW projection or demote them to explicit closure constants.",
            "priority": 3,
        },
        {
            "gate": "GR_limit_and_local_branch",
            "current_status": "cosmology branch tested separately from local PPN derivation",
            "must_derive_or_verify": "Show the same parent structure reduces to GR/Newton locally without smuggling a plateau axiom.",
            "priority": 4,
        },
        {
            "gate": "robustness_expansion",
            "current_status": "SN+BAO background robustness started; CMB/growth not yet in this scorecard",
            "must_derive_or_verify": "Extend the same discipline to growth/CMB/BAO covariance releases only after the closure claim ceiling is enforced.",
            "priority": 5,
        },
    ]


def claim_ceiling_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_type": "allowed",
            "language": "canonical_R_closure is a competitive empirical SN+BAO background closure contender",
            "condition": "Use only with the full warning labels: fitted amplitude, no parent-action promotion, DR1 weakening noted.",
        },
        {
            "claim_type": "allowed",
            "language": "MTS survives this robustness card on points, especially against wCDM/CPL-style baselines",
            "condition": "Treat as scorecard language, not proof language.",
        },
        {
            "claim_type": "forbidden",
            "language": "MTS predicts the cosmological amplitude from first principles",
            "condition": "Forbidden until B_mem or DeltaR is derived from the parent action and normalization.",
        },
        {
            "claim_type": "forbidden",
            "language": "canonical_R_closure is already a unified field theory",
            "condition": "Forbidden until the same parent branch proves covariance, conservation, GR/Newton limit, and local PPN silence.",
        },
    ]


def next_theory_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "target": "B_mem_or_DeltaR_amplitude_derivation",
            "why_it_matters": "This is the belt, not another round: the fit is competitive, but the amplitude is still owned by data.",
            "pass_condition": "A parent action fixes the amplitude scale without retuning to SN+BAO.",
            "fail_condition": "Amplitude remains an empirical closure parameter.",
        },
        {
            "rank": 2,
            "target": "canonical_R_normalization_and_aF",
            "why_it_matters": "R and a_F=1 set the ruler used by the closure branch.",
            "pass_condition": "Normalization follows from field metric, trace/Ward identity, or boundary charge.",
            "fail_condition": "Normalization is declared by convention only.",
        },
        {
            "rank": 3,
            "target": "p3_u3quarter_projection_origin",
            "why_it_matters": "T2 says the fixed shape survives, but survival is not derivation.",
            "pass_condition": "p=3 and u3=1/4 fall out of FLRW memory projection or local-to-cosmology averaging.",
            "fail_condition": "They remain selected closure constants.",
        },
        {
            "rank": 4,
            "target": "shared_GR_local_limit",
            "why_it_matters": "The theory must reduce to GR/Newton locally, not merely fit cosmology.",
            "pass_condition": "The same parent action gives local PPN silence/conservation without a smuggled plateau axiom.",
            "fail_condition": "Cosmology and local GR remain separate closures.",
        },
    ]


def decision_rows(robustness: list[dict[str, Any]], instabilities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "decision": "cosmology_status",
            "value": "survives_as_competitive_empirical_closure_not_promoted",
        },
        {
            "decision": "boxing_card",
            "value": "Mayweather-style contender: survives the card, wins style/parsimony rounds, no knockout, no belt yet",
        },
        {
            "decision": "strongest_allowed_claim",
            "value": "canonical_R_closure is an edge-free primary SN+BAO empirical closure contender with robustness warnings",
        },
        {
            "decision": "forbidden_claim",
            "value": "MTS has derived or proven the cosmological amplitude from a fundamental field theory",
        },
        {
            "decision": "main_positive_evidence",
            "value": "T1 full-covariance score survives; T2 ablations do not displace fixed shape; T3 diagonal does not reverse pattern",
        },
        {
            "decision": "main_warning",
            "value": "small-sample branches edge-hit and DR1 weakens the LCDM/AIC round",
        },
        {
            "decision": "instability_count",
            "value": str(len(instabilities)),
        },
        {
            "decision": "next_target",
            "value": "return_to_theory_gate_Bmem_amplitude_and_canonical_R_normalization",
        },
    ]


def main() -> None:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{timestamp}-canonical-R-cosmology-robustness-summary"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    missing = [row["path"] for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"Missing robustness summary sources: {missing}")

    robustness = robustness_rows()
    primary_scores = primary_score_rows()
    instabilities = instability_rows()
    theory_gates = theory_gate_rows()
    claim_ceiling = claim_ceiling_rows()
    next_theory_gates = next_theory_gate_rows()
    decisions = decision_rows(robustness, instabilities)

    write_csv(results_dir / "source_register.csv", sources, ["label", "path", "exists", "kind"])
    write_csv(results_dir / "source_checkpoint_register.csv", sources, ["label", "path", "exists", "kind"])
    write_csv(
        results_dir / "robustness_rounds.csv",
        robustness,
        ["test", "verdict", "scorecard_role", "positive_read", "warning", "claim_allowed"],
    )
    write_csv(
        results_dir / "robustness_gates.csv",
        robustness,
        ["test", "verdict", "scorecard_role", "positive_read", "warning", "claim_allowed"],
    )
    write_csv(results_dir / "primary_score_extract.csv", primary_scores, ["topic", "delta_chi2", "delta_AIC", "delta_BIC", "readout"])
    write_csv(results_dir / "instability_register.csv", instabilities, ["source", "branch_or_release", "model", "parameter", "best_fit", "interpretation"])
    write_csv(results_dir / "theory_gate_register.csv", theory_gates, ["gate", "current_status", "must_derive_or_verify", "priority"])
    write_csv(results_dir / "claim_ceiling_register.csv", claim_ceiling, ["claim_type", "language", "condition"])
    write_csv(results_dir / "next_theory_gate.csv", next_theory_gates, ["rank", "target", "why_it_matters", "pass_condition", "fail_condition"])
    write_csv(results_dir / "decision.csv", decisions, ["decision", "value"])

    status = {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "readout": "cosmology_survives_as_empirical_closure_not_promoted",
        "rounds_summarized": len(robustness),
        "instabilities_recorded": len(instabilities),
        "claim_ceiling": "empirical_closure_scorecard_only",
        "empirical_evidence_allowed": True,
        "theory_promotion_allowed": False,
        "next_action": "return_to_theory_gate_Bmem_amplitude_and_canonical_R_normalization",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
