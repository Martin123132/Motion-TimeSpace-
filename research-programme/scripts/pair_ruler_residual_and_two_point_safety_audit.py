#!/usr/bin/env python3
"""Audit fixed pair-ruler residuals and two-point safety requirements."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

SMOKE_RUN = RUNS_ROOT / "20260531-235959-fixed-pair-ruler-branch-smoke"
SMOKE_RESULTS = SMOKE_RUN / "results"
PAIR_BRANCH = "MTS_pair_ruler_fixed_u3quarter"
NO_CLOCK = "MTS_2over27_no_clock_u3quarter"
CLAIM_CEILING = "pair_ruler_residual_safety_audit_no_bridge_promotion"
STATUS = "pair_ruler_survives_but_residual_pressure_and_two_point_safety_open"


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
    if name.startswith("165-") or name.endswith("pair_ruler_residual_and_two_point_safety_audit.py"):
        return "current residual/safety audit"
    if name.startswith("164-") or "fixed-pair-ruler-branch-smoke" in str(path):
        return "fixed pair-ruler smoke evidence"
    if name.startswith("163-"):
        return "effective pair-action owner"
    if name.startswith("162-"):
        return "pair-ruler null-response contract"
    if name.startswith("161-"):
        return "trace/quadrupole source-law attempt"
    return "supporting source"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "161-trace-quadrupole-source-law-attempt.md",
        WORK_DIR / "162-pair-ruler-operator-null-response-contract.md",
        WORK_DIR / "163-effective-pair-action-owner-attempt.md",
        WORK_DIR / "164-fixed-pair-ruler-branch-smoke.md",
        SMOKE_RUN / "status.json",
        SMOKE_RESULTS / "sn_bao_fit_summary.csv",
        SMOKE_RESULTS / "sn_bao_baseline_comparison.csv",
        SMOKE_RESULTS / "pair_projection_factors.csv",
        SMOKE_RESULTS / "bao_residuals.csv",
        SMOKE_RESULTS / "sn_residual_summary.csv",
        SMOKE_RESULTS / "hz_baseline_comparison.csv",
        SMOKE_RESULTS / "gate_results.csv",
        SMOKE_RESULTS / "decision.csv",
    ]
    rows = []
    for path in paths:
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


def fit_by_branch() -> dict[str, dict[str, str]]:
    return {row["branch"]: row for row in read_csv_rows(SMOKE_RESULTS / "sn_bao_fit_summary.csv")}


def chi2_pressure_rows() -> list[dict[str, Any]]:
    fits = fit_by_branch()
    rows = []
    for reference in ["LCDM", "wCDM", "CPL", "MTS_2over27_no_clock_u3fit", NO_CLOCK]:
        pair = fits[PAIR_BRANCH]
        ref = fits[reference]
        rows.append(
            {
                "branch": PAIR_BRANCH,
                "reference_branch": reference,
                "delta_chi2_SN": float(pair["chi2_SN"]) - float(ref["chi2_SN"]),
                "delta_chi2_BAO": float(pair["chi2_BAO"]) - float(ref["chi2_BAO"]),
                "delta_chi2_total": float(pair["chi2_total"]) - float(ref["chi2_total"]),
                "delta_BIC": float(pair["BIC"]) - float(ref["BIC"]),
                "delta_Omega_m": float(pair["Omega_m"]) - float(ref["Omega_m"]),
                "dominant_pressure": "SN" if abs(float(pair["chi2_SN"]) - float(ref["chi2_SN"])) > abs(float(pair["chi2_BAO"]) - float(ref["chi2_BAO"])) else "BAO",
                "readout": "pair_better" if float(pair["BIC"]) - float(ref["BIC"]) < 0 else "pair_worse_or_draw",
            }
        )
    return rows


def bao_row_delta_rows() -> list[dict[str, Any]]:
    residuals = read_csv_rows(SMOKE_RESULTS / "bao_residuals.csv")
    projections = {int(row["row_index"]): row for row in read_csv_rows(SMOKE_RESULTS / "pair_projection_factors.csv")}
    by_branch_row = {(row["branch"], int(row["row_index"])): row for row in residuals}
    rows: list[dict[str, Any]] = []
    for reference in ["LCDM", NO_CLOCK]:
        for row_index in sorted({int(row["row_index"]) for row in residuals if row["branch"] == PAIR_BRANCH}):
            pair = by_branch_row[(PAIR_BRANCH, row_index)]
            ref = by_branch_row[(reference, row_index)]
            projection = projections[row_index]
            delta_contrib = float(pair["cov_signed_chi2_contribution"]) - float(ref["cov_signed_chi2_contribution"])
            rows.append(
                {
                    "comparison": f"pair_vs_{reference}",
                    "row_index": row_index,
                    "z": float(pair["z"]),
                    "observable": pair["observable"],
                    "Pi_perp": float(projection["Pi_perp"]),
                    "Pi_parallel": float(projection["Pi_parallel"]),
                    "pair_residual": float(pair["residual"]),
                    "reference_residual": float(ref["residual"]),
                    "delta_residual": float(pair["residual"]) - float(ref["residual"]),
                    "pair_diagonal_pull": float(pair["diagonal_pull"]),
                    "reference_diagonal_pull": float(ref["diagonal_pull"]),
                    "pair_cov_signed_chi2_contribution": float(pair["cov_signed_chi2_contribution"]),
                    "reference_cov_signed_chi2_contribution": float(ref["cov_signed_chi2_contribution"]),
                    "delta_cov_signed_chi2_contribution": delta_contrib,
                    "readout": "row_worse" if delta_contrib > 0.0 else "row_better",
                }
            )
    return rows


def observable_pressure_summary(row_deltas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in row_deltas:
        grouped[(str(row["comparison"]), str(row["observable"]))].append(row)
    rows: list[dict[str, Any]] = []
    for (comparison, observable), group in sorted(grouped.items()):
        total = sum(float(row["delta_cov_signed_chi2_contribution"]) for row in group)
        worst = max(group, key=lambda row: float(row["delta_cov_signed_chi2_contribution"]))
        best = min(group, key=lambda row: float(row["delta_cov_signed_chi2_contribution"]))
        rows.append(
            {
                "comparison": comparison,
                "observable": observable,
                "row_count": len(group),
                "sum_delta_cov_signed_chi2": total,
                "mean_delta_cov_signed_chi2": total / len(group),
                "worst_row_index": worst["row_index"],
                "worst_row_z": worst["z"],
                "worst_delta": worst["delta_cov_signed_chi2_contribution"],
                "best_row_index": best["row_index"],
                "best_row_z": best["z"],
                "best_delta": best["delta_cov_signed_chi2_contribution"],
                "readout": "net_worse" if total > 0.0 else "net_better",
            }
        )
    return rows


def worst_pressure_rows(row_deltas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for comparison in sorted({row["comparison"] for row in row_deltas}):
        group = [row for row in row_deltas if row["comparison"] == comparison]
        for rank, row in enumerate(sorted(group, key=lambda item: float(item["delta_cov_signed_chi2_contribution"]), reverse=True)[:6], start=1):
            rows.append(
                {
                    "comparison": comparison,
                    "rank": rank,
                    "row_index": row["row_index"],
                    "z": row["z"],
                    "observable": row["observable"],
                    "Pi_perp": row["Pi_perp"],
                    "Pi_parallel": row["Pi_parallel"],
                    "delta_residual": row["delta_residual"],
                    "delta_cov_signed_chi2_contribution": row["delta_cov_signed_chi2_contribution"],
                    "diagnosis": diagnose_row(row),
                }
            )
    return rows


def diagnose_row(row: dict[str, Any]) -> str:
    observable = str(row["observable"])
    z_value = float(row["z"])
    delta = float(row["delta_cov_signed_chi2_contribution"])
    if delta <= 0.0:
        return "projection_helps_this_row"
    if observable == "DM_over_rs" and z_value <= 0.6:
        return "low_z_transverse_overcorrection_or_shared_alpha_tension"
    if observable == "DH_over_rs" and z_value >= 2.0:
        return "high_z_radial_overcorrection"
    if observable == "DH_over_rs":
        return "radial_shape_pressure"
    if observable == "DM_over_rs":
        return "transverse_shape_pressure"
    return "volume_average_shape_pressure"


def safety_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_arena": "BAO row residuals",
            "why_required": "fixed pair law currently draws no-clock but worsens selected rows",
            "current_evidence": "164 residual audit",
            "risk_if_ignored": "projection only redistributes chi2",
            "next_action": "row/split audit and possible source-law repair",
            "status": "active_next",
        },
        {
            "test_arena": "growth/RSD",
            "why_required": "connected pair action may affect two-point clustering velocities",
            "current_evidence": "not tested for pair branch",
            "risk_if_ignored": "BAO-only hidden patch",
            "next_action": "define fixed pair response for fσ8/RSD or prove suppression",
            "status": "open_mandatory",
        },
        {
            "test_arena": "lensing correlations",
            "why_required": "two-point matter/ruler operator may affect correlation observables",
            "current_evidence": "not tested",
            "risk_if_ignored": "uncontrolled equivalence/geodesic tension",
            "next_action": "contract whether lensing is null or gets a derived response",
            "status": "open_mandatory",
        },
        {
            "test_arena": "CMB sound horizon",
            "why_required": "BAO ruler must not secretly recalibrate r_d",
            "current_evidence": "late-ruler condition only",
            "risk_if_ignored": "hidden CMB calibration patch",
            "next_action": "late-turn-on or Boltzmann interface proof",
            "status": "open_mandatory",
        },
        {
            "test_arena": "local/PPN",
            "why_required": "pair operator must vanish in bound domains",
            "current_evidence": "conditional local silence from coherent-domain rule",
            "risk_if_ignored": "local rods/clocks get pair-sector hair",
            "next_action": "connect compensated kernel to bound-domain X_D=0",
            "status": "conditional",
        },
        {
            "test_arena": "SN/H(z)",
            "why_required": "null response must remain stable under refit",
            "current_evidence": "H(z) exactly null; SN shifts by +1.007 chi2 from shared Omega_m refit",
            "risk_if_ignored": "one-point leakage hidden in parameter refit",
            "next_action": "profile Omega_m or run split with fixed no-clock Omega_m",
            "status": "warning_not_failure",
        },
    ]


def gate_rows(chi2_rows: list[dict[str, Any]], row_deltas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    vs_lcdm = next(row for row in chi2_rows if row["reference_branch"] == "LCDM")
    vs_no_clock = next(row for row in chi2_rows if row["reference_branch"] == NO_CLOCK)
    worst_no_clock = max(
        [row for row in row_deltas if row["comparison"] == f"pair_vs_{NO_CLOCK}"],
        key=lambda row: float(row["delta_cov_signed_chi2_contribution"]),
    )
    improved_rows = sum(
        1 for row in row_deltas if row["comparison"] == f"pair_vs_{NO_CLOCK}" and float(row["delta_cov_signed_chi2_contribution"]) < 0.0
    )
    worsened_rows = sum(
        1 for row in row_deltas if row["comparison"] == f"pair_vs_{NO_CLOCK}" and float(row["delta_cov_signed_chi2_contribution"]) > 0.0
    )
    return [
        {
            "gate": "survives_LCDM",
            "status": "pass",
            "evidence": f"delta_BIC_vs_LCDM={vs_lcdm['delta_BIC']}",
        },
        {
            "gate": "beats_no_clock_control",
            "status": "fail_draw_only",
            "evidence": f"delta_BIC_vs_no_clock={vs_no_clock['delta_BIC']}; delta_chi2_BAO={vs_no_clock['delta_chi2_BAO']}; delta_chi2_SN={vs_no_clock['delta_chi2_SN']}",
        },
        {
            "gate": "row_pressure_identified",
            "status": "pass",
            "evidence": f"worst vs no-clock row z={worst_no_clock['z']} observable={worst_no_clock['observable']} delta={worst_no_clock['delta_cov_signed_chi2_contribution']}",
        },
        {
            "gate": "row_balance",
            "status": "mixed",
            "evidence": f"vs no-clock improved_rows={improved_rows}; worsened_rows={worsened_rows}",
        },
        {
            "gate": "two_point_safety",
            "status": "fail_open",
            "evidence": "growth/RSD, lensing, and CMB ruler safety not yet tested for the pair operator",
        },
        {
            "gate": "source_law_repair",
            "status": "open",
            "evidence": "low-z transverse and high-z radial pressure may require source-law refinement, not fitted amplitude",
        },
        {
            "gate": "promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(chi2_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    vs_lcdm = next(row for row in chi2_rows if row["reference_branch"] == "LCDM")
    vs_no_clock = next(row for row in chi2_rows if row["reference_branch"] == NO_CLOCK)
    return [
        {
            "item": "status",
            "verdict": STATUS,
            "evidence": f"beats LCDM by BIC {vs_lcdm['delta_BIC']} but loses/draws no-clock by BIC {vs_no_clock['delta_BIC']}",
        },
        {
            "item": "main_empirical_readout",
            "verdict": "live_subroute_not_lead_branch",
            "evidence": "fixed pair-ruler survives but no-clock MTS remains the cleaner empirical control",
        },
        {
            "item": "main_residual_pressure",
            "verdict": "low_z_transverse_and_high_z_radial_shape_pressure",
            "evidence": "row audit identifies z=0.51 DM and z=2.33 DH pressure against no-clock",
        },
        {
            "item": "do_not_do",
            "verdict": "do_not_fit_projection_amplitudes_yet",
            "evidence": "that would turn the branch back into a BAO repair unless parent-derived",
        },
        {
            "item": "two_point_safety",
            "verdict": "mandatory_before_any_bridge_claim",
            "evidence": "pair action may affect growth/RSD/lensing/two-point observables",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "residual/safety audit only; no bridge/CMB/local-GR promotion",
        },
        {
            "item": "next_target",
            "verdict": "166-pair-ruler-row-repair-or-demotion-gate.md",
            "evidence": "try a parent-constrained row-shape repair, or freeze pair-ruler as non-leading closure while testing no-clock branch",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-pair-ruler-residual-and-two-point-safety-audit"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    chi2_rows = chi2_pressure_rows()
    row_deltas = bao_row_delta_rows()
    observable_rows = observable_pressure_summary(row_deltas)
    worst_rows = worst_pressure_rows(row_deltas)
    safety_rows = safety_matrix_rows()
    gates = gate_rows(chi2_rows, row_deltas)
    decisions = decision_rows(chi2_rows)

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "chi2_pressure_summary.csv",
        chi2_rows,
        ["branch", "reference_branch", "delta_chi2_SN", "delta_chi2_BAO", "delta_chi2_total", "delta_BIC", "delta_Omega_m", "dominant_pressure", "readout"],
    )
    write_csv(
        results_dir / "bao_row_delta_vs_controls.csv",
        row_deltas,
        [
            "comparison",
            "row_index",
            "z",
            "observable",
            "Pi_perp",
            "Pi_parallel",
            "pair_residual",
            "reference_residual",
            "delta_residual",
            "pair_diagonal_pull",
            "reference_diagonal_pull",
            "pair_cov_signed_chi2_contribution",
            "reference_cov_signed_chi2_contribution",
            "delta_cov_signed_chi2_contribution",
            "readout",
        ],
    )
    write_csv(
        results_dir / "bao_observable_pressure_summary.csv",
        observable_rows,
        [
            "comparison",
            "observable",
            "row_count",
            "sum_delta_cov_signed_chi2",
            "mean_delta_cov_signed_chi2",
            "worst_row_index",
            "worst_row_z",
            "worst_delta",
            "best_row_index",
            "best_row_z",
            "best_delta",
            "readout",
        ],
    )
    write_csv(
        results_dir / "worst_row_pressure.csv",
        worst_rows,
        ["comparison", "rank", "row_index", "z", "observable", "Pi_perp", "Pi_parallel", "delta_residual", "delta_cov_signed_chi2_contribution", "diagnosis"],
    )
    write_csv(
        results_dir / "two_point_safety_test_matrix.csv",
        safety_rows,
        ["test_arena", "why_required", "current_evidence", "risk_if_ignored", "next_action", "status"],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status = {
        "status": STATUS,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "generated": [
            "source_register.csv",
            "chi2_pressure_summary.csv",
            "bao_row_delta_vs_controls.csv",
            "bao_observable_pressure_summary.csv",
            "worst_row_pressure.csv",
            "two_point_safety_test_matrix.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "166-pair-ruler-row-repair-or-demotion-gate.md",
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
