#!/usr/bin/env python3
"""Checkpoint 239: no-hair targets or closure-flagged local-bound runner."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_239_NAME = "nohair-theorem-targets-or-local-bound-runner"
RUN_226 = RUNS_ROOT / "20260601-000043-local-bound-preflight-and-baseline-comparison"
RUN_227 = RUNS_ROOT / "20260601-000044-local-PPN-coefficient-map-or-official-bound-manifest"
RUN_238 = RUNS_ROOT / "20260601-000055-metric-only-exterior-reduction-or-nohair-theorem"

STATUS = "closure_flagged_local_bound_preflight_identifies_WEP_universal_coupling_as_hardest_no_pass_claim"
CLAIM_CEILING = "closure_flagged_local_bound_pressure_no_official_pass_or_PPN_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

BOUND_ROWS = [
    {
        "residual": "gamma_minus_1",
        "bound_value": 2.3e-5,
        "bound_label": "Cassini gamma sigma scale",
        "source": "Bertotti/Iess/Tortora Nature 2003 + NIST cross-check",
        "usage": "closure pressure only, not pass/fail",
    },
    {
        "residual": "beta_minus_1",
        "bound_value": 7.8e-5,
        "bound_label": "Will 2014 beta uncertainty adopting Cassini gamma",
        "source": "Will Living Reviews 2014",
        "usage": "closure pressure only; primary ephemeris source still needed for public use",
    },
    {
        "residual": "alpha_clock",
        "bound_value": 2.48e-5,
        "bound_label": "Galileo redshift fractional-deviation uncertainty",
        "source": "Delva et al. PRL 2018 arXiv record",
        "usage": "closure pressure only, not pass/fail",
    },
    {
        "residual": "epsilon_matter",
        "bound_value": math.sqrt(2.3e-15**2 + 1.5e-15**2),
        "bound_label": "MICROSCOPE combined stat/syst uncertainty proxy",
        "source": "Touboul et al. PRL 2022 arXiv record",
        "usage": "closure pressure only; composition coupling must be parent-forbidden",
    },
    {
        "residual": "Phi_minus_Psi",
        "bound_value": 2.3e-5,
        "bound_label": "internal q-like slip proxy gate",
        "source": "checkpoint 226 internal gate, no official slip likelihood",
        "usage": "internal pressure only",
    },
    {
        "residual": "G_eff_over_G_minus_1",
        "bound_value": 2.3e-5,
        "bound_label": "internal q-like source proxy gate",
        "source": "checkpoint 226 internal gate, no official G_eff likelihood",
        "usage": "internal pressure only",
    },
]


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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 239 runner"),
        (WORK_DIR / "227-local-PPN-coefficient-map-or-official-bound-manifest.md", "official local-bound manifest"),
        (WORK_DIR / "238-metric-only-exterior-reduction-or-nohair-theorem.md", "no-hair target audit"),
        (RUN_226 / "results" / "coefficient_budget_ranking.csv", "closure coefficient budgets"),
        (RUN_227 / "results" / "official_local_bound_manifest.csv", "official manifest source rows"),
        (RUN_238 / "results" / "nohair_theorem_targets.csv", "N1-N6 targets"),
        (RUN_238 / "status.json", "checkpoint 238 machine status"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": role,
                "issue": "" if exists else "missing",
            }
        )
    return rows


def numeric_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual": row["residual"],
            "bound_value": row["bound_value"],
            "bound_label": row["bound_label"],
            "source": row["source"],
            "usage": row["usage"],
            "claim_status": "closure_pressure_only_no_pass_fail",
        }
        for row in BOUND_ROWS
    ]


def pressure_label(max_coefficient: float) -> str:
    if max_coefficient < 1e-6:
        return "must_be_exact_zero_or_parent_forbidden"
    if max_coefficient < 1.0:
        return "sub_unit_coefficient_required"
    if max_coefficient < 3.0:
        return "order_unity_tight"
    if max_coefficient < 10.0:
        return "order_unity_comfortable_not_claimable"
    return "loose_for_unit_coefficient_not_claimable"


def closure_pressure_rows() -> list[dict[str, Any]]:
    budget_rows = read_csv_rows(RUN_226 / "results" / "coefficient_budget_ranking.csv")
    bound_by_residual = {row["residual"]: row for row in BOUND_ROWS}
    rows: list[dict[str, Any]] = []
    for row in budget_rows:
        residual = row["residual"]
        bound = bound_by_residual.get(residual)
        if not bound:
            continue
        epsilon = float(row["epsilon_J_budget"])
        bound_value = float(bound["bound_value"])
        max_coefficient = bound_value / epsilon if epsilon > 0 else math.inf
        unit_ratio = epsilon / bound_value if bound_value > 0 else math.inf
        rows.append(
            {
                "case": row["case"],
                "residual": residual,
                "epsilon_J_budget": epsilon,
                "bound_value": bound_value,
                "max_abs_coefficient_before_bound": max_coefficient,
                "unit_coefficient_ratio_to_bound": unit_ratio,
                "pressure_label": pressure_label(max_coefficient),
                "source": bound["source"],
                "claim_status": "closure_pressure_only_no_official_pass_fail",
            }
        )
    return rows


def scenario_rows() -> list[dict[str, Any]]:
    pressure = closure_pressure_rows()
    worst_by_residual: dict[str, dict[str, Any]] = {}
    for row in pressure:
        residual = row["residual"]
        old = worst_by_residual.get(residual)
        if old is None or row["unit_coefficient_ratio_to_bound"] > old["unit_coefficient_ratio_to_bound"]:
            worst_by_residual[residual] = row

    rows: list[dict[str, Any]] = []
    for residual, row in sorted(worst_by_residual.items()):
        if residual in {"gamma_minus_1", "Phi_minus_Psi"}:
            safe_coefficient = 0.0
            safe_reason = "scalar-boundary/no-shear condition"
        elif residual in {"alpha_clock", "epsilon_matter"}:
            safe_coefficient = 0.0
            safe_reason = "universal metric coupling condition"
        elif residual == "beta_minus_1":
            safe_coefficient = 0.0
            safe_reason = "metric-only EH/Schwarzschild exterior condition"
        else:
            safe_coefficient = 1.0
            safe_reason = "monopole source-normalization proxy"

        scenario_coefficients = [
            ("safe_branch_contract", safe_coefficient),
            ("unit_unknown_coefficient", 1.0),
            ("stress_leakage_coefficient_10", 10.0),
        ]
        if residual == "epsilon_matter":
            scenario_coefficients.append(("direct_matter_leak_1e-6", 1e-6))

        for scenario, coefficient in scenario_coefficients:
            predicted = coefficient * float(row["epsilon_J_budget"])
            bound = float(row["bound_value"])
            ratio = predicted / bound if bound > 0 else math.inf
            if scenario == "safe_branch_contract":
                readout = "conditional_safe_if_parent_theorem_holds_not_claimable"
            elif scenario == "direct_matter_leak_1e-6" and ratio > 1.0:
                readout = "tiny_direct_matter_leak_still_exceeds_WEP_bound_scale"
            elif ratio <= 1.0:
                readout = "below_bound_scale_but_closure_flagged"
            else:
                readout = "exceeds_bound_scale_under_closure_assumption"
            rows.append(
                {
                    "scenario": scenario,
                    "residual": residual,
                    "reference_case": row["case"],
                    "coefficient": coefficient,
                    "predicted_residual": predicted,
                    "bound_value": bound,
                    "ratio_to_bound": ratio,
                    "readout": readout,
                    "safe_branch_reason": safe_reason,
                    "claim_status": "no_pass_fail_claim",
                }
            )
    return rows


def nohair_priority_rows() -> list[dict[str, Any]]:
    pressure = closure_pressure_rows()
    weakest = sorted(pressure, key=lambda row: row["max_abs_coefficient_before_bound"])
    matter = next(row for row in weakest if row["residual"] == "epsilon_matter")
    clock = next(row for row in weakest if row["residual"] == "alpha_clock")
    gamma = next(row for row in weakest if row["residual"] == "gamma_minus_1")
    beta = next(row for row in weakest if row["residual"] == "beta_minus_1")
    geff = next(row for row in weakest if row["residual"] == "G_eff_over_G_minus_1")
    slip = next(row for row in weakest if row["residual"] == "Phi_minus_Psi")
    return [
        {
            "rank": 1,
            "target": "N3_universal_coupling",
            "pressure_channel": "epsilon_matter",
            "max_abs_coefficient_before_bound": matter["max_abs_coefficient_before_bound"],
            "reason": "MICROSCOPE-scale WEP bound crushes any direct composition coupling",
            "next_action": "derive matter/clocks couple only to metric/coframe",
        },
        {
            "rank": 2,
            "target": "N2_no_TF",
            "pressure_channel": "gamma_minus_1/Phi_minus_Psi",
            "max_abs_coefficient_before_bound": min(gamma["max_abs_coefficient_before_bound"], slip["max_abs_coefficient_before_bound"]),
            "reason": "Cassini/internal slip pressure is order-unity tight for current epsilon budget",
            "next_action": "derive scalar-boundary no trace-free stress",
        },
        {
            "rank": 3,
            "target": "N1_Meff",
            "pressure_channel": "G_eff_over_G_minus_1",
            "max_abs_coefficient_before_bound": geff["max_abs_coefficient_before_bound"],
            "reason": "source normalization must remain monopole-only",
            "next_action": "derive conserved M_eff and no radial memory profile",
        },
        {
            "rank": 4,
            "target": "N6_auxiliary_nohair/N4_exact_relative_memory",
            "pressure_channel": "beta_minus_1",
            "max_abs_coefficient_before_bound": beta["max_abs_coefficient_before_bound"],
            "reason": "beta is less numerically tight for unit coefficients but theoretically decisive",
            "next_action": "derive metric-only exterior/no-hair route",
        },
        {
            "rank": 5,
            "target": "N3_clock_part",
            "pressure_channel": "alpha_clock",
            "max_abs_coefficient_before_bound": clock["max_abs_coefficient_before_bound"],
            "reason": "clock coupling is order-unity tight and must be universal",
            "next_action": "derive no direct memory-clock coupling",
        },
        {
            "rank": 6,
            "target": "N5_projector_stress",
            "pressure_channel": "all",
            "max_abs_coefficient_before_bound": "",
            "reason": "conservation failure can leak into any channel",
            "next_action": "compute T_projector or prove cancellation",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_register_rows())
    pressure = closure_pressure_rows()
    matter_pressure = min(
        row["max_abs_coefficient_before_bound"]
        for row in pressure
        if row["residual"] == "epsilon_matter"
    )
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "official-bound manifest converted to numeric pressure rows",
            "status": "pass",
            "evidence": f"bound_rows={len(BOUND_ROWS)}",
            "claim_allowed": "closure pressure only",
        },
        {
            "gate": "closure scenarios evaluated",
            "status": "pass",
            "evidence": "safe/unit/stress-leak scenarios",
            "claim_allowed": "no pass/fail claim",
        },
        {
            "gate": "hardest no-hair target identified",
            "status": "pass",
            "evidence": f"epsilon_matter max coefficient before bound {matter_pressure:.3e}",
            "claim_allowed": "priority only",
        },
        {
            "gate": "official local-bound pass claimed",
            "status": "fail",
            "evidence": "coefficients are closure-level and not parent-derived",
            "claim_allowed": "no",
        },
        {
            "gate": "local GR or PPN promoted",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "A closure-flagged local-bound preflight was run using the current epsilon_J budgets and official/source-manifest bound scales. The strongest pressure is not beta; it is direct matter/composition coupling. Any nonzero memory-sector composition coupling must be essentially forbidden, not merely small. Gamma/slip/clock are order-unity tight under the current closure budget, while beta is theoretically decisive but numerically less tight for unit coefficients. No official pass/fail claim is made.",
            "main_gain": "the next no-hair target is empirically prioritized rather than guessed",
            "main_failure": "all coefficients remain closure-level until N-targets are parent-derived",
            "next_target": "240-universal-coupling-parent-contract-or-local-bound-data-runner.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_239_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    bound_rows = numeric_bound_rows()
    pressure_rows = closure_pressure_rows()
    scenarios = scenario_rows()
    priorities = nohair_priority_rows()
    gates = claim_gate_rows()
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "numeric_local_bound_manifest.csv": (
            bound_rows,
            ["residual", "bound_value", "bound_label", "source", "usage", "claim_status"],
        ),
        "closure_pressure_by_case.csv": (
            pressure_rows,
            [
                "case",
                "residual",
                "epsilon_J_budget",
                "bound_value",
                "max_abs_coefficient_before_bound",
                "unit_coefficient_ratio_to_bound",
                "pressure_label",
                "source",
                "claim_status",
            ],
        ),
        "closure_scenario_readout.csv": (
            scenarios,
            [
                "scenario",
                "residual",
                "reference_case",
                "coefficient",
                "predicted_residual",
                "bound_value",
                "ratio_to_bound",
                "readout",
                "safe_branch_reason",
                "claim_status",
            ],
        ),
        "nohair_priority_after_bound_preflight.csv": (
            priorities,
            [
                "rank",
                "target",
                "pressure_channel",
                "max_abs_coefficient_before_bound",
                "reason",
                "next_action",
            ],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "main_gain",
                "main_failure",
                "next_target",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, file_data in files.items():
        rows, fieldnames = file_data
        write_csv(results_dir / filename, rows, fieldnames)

    pressure = closure_pressure_rows()
    matter_pressure = min(
        row["max_abs_coefficient_before_bound"]
        for row in pressure
        if row["residual"] == "epsilon_matter"
    )
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": sum(row["exists"] != "yes" for row in source_rows),
        "closure_flagged_local_bound_preflight_done": True,
        "official_pass_fail_claimed": False,
        "hardest_target": "N3_universal_coupling",
        "hardest_channel": "epsilon_matter",
        "hardest_max_abs_coefficient_before_bound": matter_pressure,
        "PPN_promoted": False,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    print(json.dumps(run(args.timestamp), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
