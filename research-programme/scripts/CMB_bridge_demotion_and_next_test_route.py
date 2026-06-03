"""Demote the compressed-CMB bridge and choose the next fair test route."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

WORK_DIR = Path(__file__).resolve().parent.parent
RUNS_ROOT = WORK_DIR / "runs"

RUN_121 = RUNS_ROOT / "20260531-171500-shared-calibration-relation-attempt"
RUN_122 = RUNS_ROOT / "20260531-172300-early-late-Omega-map-theorem-attempt"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        RUN_121 / "results" / "decision.csv",
        RUN_121 / "results" / "aggregate_targets.csv",
        RUN_122 / "results" / "decision.csv",
        RUN_122 / "results" / "aggregate_map_diagnostics.csv",
        RUN_122 / "results" / "candidate_map_audit.csv",
        WORK_DIR / "121-shared-calibration-relation-derivation-attempt.md",
        WORK_DIR / "122-early-late-Omega-map-theorem-attempt.md",
        script_path,
    ]
    return [
        {
            "source": path.name,
            "path": str(path),
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path in paths
    ]


def previous_gate_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_label, path in [
        ("checkpoint_121", RUN_121 / "results" / "decision.csv"),
        ("checkpoint_122", RUN_122 / "results" / "decision.csv"),
    ]:
        for row in read_csv_rows(path):
            rows.append(
                {
                    "source": source_label,
                    "item": row["item"],
                    "verdict": row["verdict"],
                    "evidence": row["evidence"],
                }
            )
    return rows


def route_scorecard_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "continue_compressed_CMB_background_priors",
            "targets_current_failure": "partial",
            "near_term_cost": "low",
            "theory_value": "low",
            "claim_risk": "high",
            "fairness_status": "demoted",
            "recommended_order": "",
            "decision": "do_not_use_for_promotion",
            "reason": "compressed priors gave draws/mixed gates but the Omega map is not derived and is likelihood-response dependent",
        },
        {
            "route": "BAO_shape_residual_decomposition",
            "targets_current_failure": "direct",
            "near_term_cost": "low_medium",
            "theory_value": "medium",
            "claim_risk": "low",
            "fairness_status": "apply_to_LCDM_wCDM_CPL_MTS",
            "recommended_order": 1,
            "decision": "run_next",
            "reason": "checkpoint 121 found the live residual is BAO shape after Omega_m0 shifts, and existing SN+BAO data are already loaded",
        },
        {
            "route": "growth_or_Hz_non_CMB_stress_test",
            "targets_current_failure": "indirect",
            "near_term_cost": "medium",
            "theory_value": "medium_high",
            "claim_risk": "medium",
            "fairness_status": "needs_data_manifest_and_baselines",
            "recommended_order": 2,
            "decision": "queue_after_BAO_shape",
            "reason": "independent expansion/growth tests reduce dependence on compressed CMB priors",
        },
        {
            "route": "full_CMB_perturbation_acoustic_contract",
            "targets_current_failure": "direct_high_value",
            "near_term_cost": "high",
            "theory_value": "very_high",
            "claim_risk": "medium_high",
            "fairness_status": "requires_official_likelihood_or_Boltzmann_implementation",
            "recommended_order": 3,
            "decision": "write_contract_before_running",
            "reason": "this is the proper CMB route, but it is too expensive to treat as a quick next test",
        },
        {
            "route": "local_GR_PPN_derivation",
            "targets_current_failure": "separate_mandatory_theory_gate",
            "near_term_cost": "high",
            "theory_value": "very_high",
            "claim_risk": "low_if_kept_private",
            "fairness_status": "not_a_cosmology_score",
            "recommended_order": "parallel",
            "decision": "keep_as_parallel_spine_requirement",
            "reason": "unified theory still needs local GR reduction, but it does not answer the present BAO/CMB residual",
        },
        {
            "route": "matter_memory_exchange_Qnu_theorem",
            "targets_current_failure": "direct_if_successful",
            "near_term_cost": "high",
            "theory_value": "very_high",
            "claim_risk": "high",
            "fairness_status": "must_preserve_Bianchi_and_PPN",
            "recommended_order": "parallel_after_BAO_shape",
            "decision": "do_not_fit_until_derived",
            "reason": "a nontrivial Omega map requires Q^nu, but introducing Q^nu without derivation would be an ad hoc rescue",
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "compressed_CMB_claim_ceiling",
            "rule": "compressed CMB background priors cannot promote the theory branch",
            "status": "locked",
        },
        {
            "gate": "baseline_symmetry",
            "rule": "BAO-shape decomposition must score LCDM, wCDM, CPL, MTS_locked, and Bmem_zero with identical rows/covariance",
            "status": "required",
        },
        {
            "gate": "no_private_rescue",
            "rule": "no MTS-only BAO deformation may be scored before a derivation contract exists",
            "status": "required",
        },
        {
            "gate": "observable_decomposition",
            "rule": "separate DM/rs, DH/rs, DV/rs residual contributions and redshift leverage",
            "status": "required",
        },
        {
            "gate": "promotion_wording",
            "rule": "allowed wording is survival/draw/closure; forbidden wording is passes CMB or derived Omega map",
            "status": "locked",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "compressed_CMB_bridge",
            "verdict": "demoted_to_empirical_closure",
            "evidence": "checkpoint 122 rejected a background-only Omega map theorem under current assumptions",
        },
        {
            "item": "next_test",
            "verdict": "BAO_shape_residual_decomposition",
            "evidence": "directly targets the current failure and can be run fairly on existing data/baselines",
        },
        {
            "item": "next_theory",
            "verdict": "Qnu_or_acoustic_shape_contract_only_after_residual_map",
            "evidence": "the residual must be localized before attempting a high-cost perturbation/acoustic derivation",
        },
        {
            "item": "claim_status",
            "verdict": "not_promoted_not_dead",
            "evidence": "late SN+BAO and BAO-only remain alive; compressed CMB bridge is mixed/closure-only",
        },
        {
            "item": "next_target",
            "verdict": "124-BAO-shape-residual-decomposition.md plus script",
            "evidence": "score the exact observable/redshift rows driving the BAO shape penalty",
        },
    ]


def run_gate(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-CMB-bridge-demotion-and-next-test-route"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows(Path(__file__).resolve())
    if any(not row["exists"] for row in source_rows):
        missing = [row["path"] for row in source_rows if not row["exists"]]
        raise FileNotFoundError(f"missing required source files: {missing}")

    previous_rows = previous_gate_rows()
    route_rows = route_scorecard_rows()
    acceptance_rows = acceptance_gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", source_rows, ["source", "path", "exists", "issue"])
    write_csv(results_dir / "previous_gate_summary.csv", previous_rows, ["source", "item", "verdict", "evidence"])
    write_csv(
        results_dir / "route_scorecard.csv",
        route_rows,
        [
            "route",
            "targets_current_failure",
            "near_term_cost",
            "theory_value",
            "claim_risk",
            "fairness_status",
            "recommended_order",
            "decision",
            "reason",
        ],
    )
    write_csv(results_dir / "acceptance_gates.csv", acceptance_rows, ["gate", "rule", "status"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status = {
        "status": "compressed_CMB_bridge_demoted_next_route_BAO_shape_residuals",
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": "routing_gate_not_public_evidence",
        "generated": [
            "source_register.csv",
            "previous_gate_summary.csv",
            "route_scorecard.csv",
            "acceptance_gates.csv",
            "decision.csv",
        ],
        "next_target": "124-BAO-shape-residual-decomposition.md plus scripts/BAO_shape_residual_decomposition.py",
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
    print(run_gate(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
