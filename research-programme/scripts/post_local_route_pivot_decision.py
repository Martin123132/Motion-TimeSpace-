#!/usr/bin/env python3
"""Decide the next route after demoting the local Ccoh parent-action branch."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "73_local_route_blocker_gate": Path("73-local-route-blocker-ledger-and-promotion-gate.md"),
    "74_priority_decision": Path("74-next-derivation-priority-decision.md"),
    "76_Ccoh_Bianchi_identity": Path("76-Ccoh-Bianchi-identity-attempt.md"),
    "80_stress_free_reference_gate": Path("80-stress-free-reference-action-gate.md"),
    "80_decision": Path("runs/20260531-120531-stress-free-reference-action-gate/results/decision.csv"),
    "80_next_route_options": Path("runs/20260531-120531-stress-free-reference-action-gate/results/next_route_options.csv"),
    "80_demotion_register": Path("runs/20260531-120531-stress-free-reference-action-gate/results/demotion_register.csv"),
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


def pivot_option_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "amplitude_normalization_gate",
            "promotion_value": "high",
            "empirical_value": "medium",
            "risk": "can become algebraic tuning if disconnected from data",
            "why_now": "u3/p=3/B_mem/amplitude normalization remains central across cosmology and local closure",
            "verdict": "selected_first",
        },
        {
            "route": "empirical_closure_testing",
            "promotion_value": "medium",
            "empirical_value": "high",
            "risk": "tests phenomenology not a completed field theory",
            "why_now": "Ccoh is demoted to closure, so it can be tested honestly without claiming derivation",
            "verdict": "selected_second",
        },
        {
            "route": "perturbation_lensing_growth_contract",
            "promotion_value": "high",
            "empirical_value": "high",
            "risk": "needs stable background and amplitude conventions first",
            "why_now": "cosmology seriousness requires perturbations, lensing, and growth against GR baselines",
            "verdict": "third_after_amplitude",
        },
        {
            "route": "new_local_GR_mechanism_search",
            "promotion_value": "very_high",
            "empirical_value": "low_initially",
            "risk": "could restart hidden-selector tunnelling",
            "why_now": "core requirement remains unsolved but no clean mechanism is currently available",
            "verdict": "park_until_new_mechanism",
        },
        {
            "route": "return_to_Ccoh_parent_route",
            "promotion_value": "low_after_gate_failure",
            "empirical_value": "low",
            "risk": "violates checkpoint-80 demotion",
            "why_now": "not justified",
            "verdict": "rejected",
        },
    ]


def decision_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "criterion": "respects_checkpoint_80_demotion",
            "amplitude": "pass",
            "empirical": "pass",
            "perturbations": "pass",
            "new_local_GR": "pass_if_not_selector",
            "winner": "amplitude_or_empirical",
        },
        {
            "criterion": "increases_field_theory_discipline",
            "amplitude": "high",
            "empirical": "medium",
            "perturbations": "high",
            "new_local_GR": "unknown",
            "winner": "amplitude",
        },
        {
            "criterion": "gets_testable_soon",
            "amplitude": "medium",
            "empirical": "high",
            "perturbations": "medium_high",
            "new_local_GR": "low",
            "winner": "empirical",
        },
        {
            "criterion": "reduces_free_parameter_risk",
            "amplitude": "high",
            "empirical": "medium",
            "perturbations": "medium",
            "new_local_GR": "unknown",
            "winner": "amplitude",
        },
        {
            "criterion": "supports_future_cosmology_robustness",
            "amplitude": "high",
            "empirical": "high",
            "perturbations": "high",
            "new_local_GR": "low_initially",
            "winner": "amplitude_then_empirical_then_perturbations",
        },
    ]


def selected_sequence_rows() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "target": "82-amplitude-normalization-gate.md",
            "purpose": "audit whether p=3/u3/B_mem/amplitude factors can be derived, bounded, or demoted to fitted closure",
            "promotion_gate": "no unexplained amplitude may be treated as derived",
        },
        {
            "rank": 2,
            "target": "83-empirical-closure-test-manifest.md",
            "purpose": "convert demoted closures into honest tests against cosmology/local/galaxy data with GR baselines",
            "promotion_gate": "closure success may motivate, not prove, field theory",
        },
        {
            "rank": 3,
            "target": "84-perturbation-lensing-growth-contract.md",
            "purpose": "write the perturbation and lensing obligations needed for serious cosmology comparison",
            "promotion_gate": "must compare against fitted GR/LambdaCDM/wCDM/CPL-style baselines where relevant",
        },
        {
            "rank": 4,
            "target": "future-new-local-GR-mechanism.md",
            "purpose": "only reopen local-GR derivation if a new mechanism does not hide behind selectors",
            "promotion_gate": "must reduce to GR without new local stress, preferred frame, or hand-selected domain",
        },
    ]


def guardrail_rows() -> list[dict[str, Any]]:
    return [
        {
            "guardrail": "no_public_local_GR_claim",
            "rule": "local GR remains not derived after checkpoint 80",
            "reason": "stress-free u/D parent owner failed",
        },
        {
            "guardrail": "closures_are_allowed_but_labelled",
            "rule": "Ccoh and related selectors may be tested as diagnostic closures only",
            "reason": "empirical value survives even when parent derivation fails",
        },
        {
            "guardrail": "baseline_fairness",
            "rule": "future empirical tests must include appropriate GR/LambdaCDM or other baseline comparisons",
            "reason": "a failed jackknife or robustness test is only meaningful relative to baseline behavior",
        },
        {
            "guardrail": "amplitude_honesty",
            "rule": "amplitude factors must be derived, bounded, or explicitly fitted",
            "reason": "unexplained normalization can fake agreement across sectors",
        },
        {
            "guardrail": "no_hidden_selector_reentry",
            "rule": "do not revive Ccoh parent route without a genuinely new mechanism",
            "reason": "checkpoint 80 already triggered the kill gate",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "post_local_route_pivot",
            "status": "pivot_to_amplitude_normalization_first_then_empirical_closure_tests",
            "evidence": "amplitude reduces free-parameter risk and empirical tests keep the demoted closures honest",
            "next_action": "create 82-amplitude-normalization-gate.md",
        },
        {
            "decision": "local_Ccoh_route_status",
            "status": "demoted_to_diagnostic_closure",
            "evidence": "checkpoint 80 stress-free reference action gate failed",
            "next_action": "do not reopen without a new non-selector mechanism",
        },
        {
            "decision": "local_GR_status",
            "status": "not_derived",
            "evidence": "no acceptable stress-free u/D parent action",
            "next_action": "keep as an explicit blocker while working amplitude/testing spine",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name,
        "readout": "pivot_to_amplitude_first_then_empirical_closure_tests",
        "key_metrics": {
            "pivot_options": counts["pivot_options"],
            "decision_matrix_rows": counts["decision_matrix"],
            "selected_sequence_steps": counts["selected_sequence"],
            "guardrails": counts["guardrails"],
            "selected_next": "82-amplitude-normalization-gate.md",
        },
        "decision": decision_rows()[0],
        "next_target": "82-amplitude-normalization-gate.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-post-local-route-pivot-decision"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "pivot_options": (
            pivot_option_rows(),
            ["route", "promotion_value", "empirical_value", "risk", "why_now", "verdict"],
        ),
        "decision_matrix": (
            decision_matrix_rows(),
            ["criterion", "amplitude", "empirical", "perturbations", "new_local_GR", "winner"],
        ),
        "selected_sequence": (
            selected_sequence_rows(),
            ["rank", "target", "purpose", "promotion_gate"],
        ),
        "guardrails": (
            guardrail_rows(),
            ["guardrail", "rule", "reason"],
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
