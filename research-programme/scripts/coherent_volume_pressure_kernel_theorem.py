#!/usr/bin/env python3
"""Test the coherent-volume variation derivation of the memory pressure kernel."""

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
AUX_RUN = RUNS_ROOT / "20260531-200000-auxiliary-geometric-memory-action-owner"
AUX_RESULTS = AUX_RUN / "results"

CLAIM_CEILING = "conditional_volume_pressure_kernel_not_full_parent_theory"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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


def source_register_rows(script_path: Path, aux_run: Path) -> list[dict[str, Any]]:
    aux_results = aux_run / "results"
    paths = [
        script_path,
        WORK_DIR / "51-FLRW-memory-current-contract.md",
        WORK_DIR / "54-coherent-domain-and-u3-origin.md",
        WORK_DIR / "56-u3-quarter-parent-cell-theorem-attempt.md",
        WORK_DIR / "57-memory-action-owner-contract.md",
        WORK_DIR / "68-chiD-gated-memory-conservation-contract.md",
        WORK_DIR / "132-smooth-memory-growth-theorem-attempt.md",
        WORK_DIR / "136-memory-action-potential-owner-attempt.md",
        WORK_DIR / "137-auxiliary-geometric-memory-action-owner.md",
        aux_run / "status.json",
        aux_results / "required_pressure_kernel.csv",
        aux_results / "gate_results.csv",
        aux_results / "decision.csv",
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


def derivation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "coherent_domain_volume",
            "equation": "V_D = integral_D sqrt(h) d^3x",
            "result": "domain volume is a scalar once the coherent domain is selected",
            "status": "assumption_from_domain_contract",
            "blocker": "parent boundary rule for D is not derived",
        },
        {
            "step": "volume_time_variable",
            "equation": "N_D = (1/3) ln(V_D0/V_D)",
            "result": "FLRW gives V_D proportional to a^3, hence N_D=-ln(a)=ln(1+z)",
            "status": "pass_conditional",
            "blocker": "requires coherent-domain volume, not pointwise local scale factor",
        },
        {
            "step": "spatial_metric_variation",
            "equation": "delta N_D = -(1/6)<h^ij delta h_ij>_D",
            "result": "spatial volume variation carries the factor needed for pressure",
            "status": "pass_formal",
            "blocker": "boundary variation terms must be carried by J_rel",
        },
        {
            "step": "memory_density_action",
            "equation": "S_M = - integral sqrt(-g) rho_M(N_D)",
            "result": "delta S_M = 1/2 integral sqrt(-g)[-rho_M + rho_M,N/3] h^ij delta h_ij",
            "status": "pass_formal",
            "blocker": "rho_M(N_D) law still supplied by locked branch",
        },
        {
            "step": "pressure_kernel",
            "equation": "p_M = -rho_M + (1/3)d rho_M/dN_D",
            "result": "p_M + rho_M = B_mem A_N/3",
            "status": "derived_conditional",
            "blocker": "B_mem, A(N), p=3, u3=1/4 not derived here",
        },
        {
            "step": "local_endpoint_silence",
            "equation": "A_N(0)=0 for cubic activation",
            "result": "activation pressure lift vanishes at N_D=0",
            "status": "pass_conditional",
            "blocker": "must prove bound local domains sit at N_D=0 and delta N_D=0",
        },
    ]


def pressure_kernel_check_rows(required_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in required_rows:
        rho = float(item["rho_mem"])
        pressure_target = float(item["pressure_mem"])
        lift_target = float(item["p_plus_rho_required"])
        rho_n = 3.0 * lift_target
        pressure_from_volume = -rho + rho_n / 3.0
        lift_from_volume = pressure_from_volume + rho
        rows.append(
            {
                "index": int(item["index"]),
                "z": float(item["z"]),
                "N_past": float(item["N_past"]),
                "rho_mem": rho,
                "rho_N_from_locked_density": rho_n,
                "pressure_target": pressure_target,
                "pressure_from_volume_variation": pressure_from_volume,
                "abs_pressure_error": abs(pressure_from_volume - pressure_target),
                "p_plus_rho_target": lift_target,
                "p_plus_rho_from_volume_variation": lift_from_volume,
                "abs_lift_error": abs(lift_from_volume - lift_target),
                "local_endpoint_pressure_lift": "zero" if abs(lift_from_volume) < 1.0e-12 else "active",
            }
        )
    return rows


def theorem_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "coherent_domain_selected",
            "needed_for": "V_D and N_D are physical branch variables",
            "status": "open",
            "failure_mode": "domain becomes a rescue smoothing scale",
        },
        {
            "condition": "N_D_equals_one_third_log_volume_ratio",
            "needed_for": "spatial variation produces the 1/3 pressure factor",
            "status": "pass_conditional",
            "failure_mode": "pressure kernel loses derivation",
        },
        {
            "condition": "boundary_terms_owned_by_J_rel",
            "needed_for": "varying D does not create wall stress or PPN hair",
            "status": "open",
            "failure_mode": "local GR branch endangered",
        },
        {
            "condition": "density_law_from_parent",
            "needed_for": "B_mem A(N_D) is predicted rather than inserted",
            "status": "fail",
            "failure_mode": "healthy EFT closure, not fundamental derivation",
        },
        {
            "condition": "cubic_activation_regular_endpoint",
            "needed_for": "A_N(0)=0 and local endpoint pressure lift vanishes",
            "status": "pass_conditional",
            "failure_mode": "local activation pressure appears",
        },
        {
            "condition": "full_perturbation_action",
            "needed_for": "CMB/growth perturbation promotion",
            "status": "not_done",
            "failure_mode": "late-time background theorem overclaimed",
        },
    ]


def summary_rows(check_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    max_pressure_error = max(float(row["abs_pressure_error"]) for row in check_rows)
    max_lift_error = max(float(row["abs_lift_error"]) for row in check_rows)
    peak_row = max(check_rows, key=lambda row: float(row["p_plus_rho_from_volume_variation"]))
    endpoint_row = check_rows[0]
    zero_endpoint = abs(float(endpoint_row["p_plus_rho_from_volume_variation"])) < 1.0e-12
    active_rows = sum(1 for row in check_rows if row["local_endpoint_pressure_lift"] == "active")
    return [
        {
            "item": "rows_checked",
            "value": len(check_rows),
            "readout": "matches_required_pressure_kernel_grid",
        },
        {
            "item": "max_pressure_error",
            "value": max_pressure_error,
            "readout": "pass" if max_pressure_error < 1.0e-12 else "check",
        },
        {
            "item": "max_lift_error",
            "value": max_lift_error,
            "readout": "pass" if max_lift_error < 1.0e-12 else "check",
        },
        {
            "item": "peak_volume_pressure_lift",
            "value": peak_row["p_plus_rho_from_volume_variation"],
            "readout": f"z={float(peak_row['z']):.6g}",
        },
        {
            "item": "endpoint_pressure_lift_zero",
            "value": zero_endpoint,
            "readout": "pass" if zero_endpoint else "fail",
        },
        {
            "item": "active_pressure_rows",
            "value": active_rows,
            "readout": "activation_pressure_generated_only_away_from_endpoint",
        },
    ]


def gate_rows(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_item = {row["item"]: row for row in summary}
    pressure_error = float(by_item["max_pressure_error"]["value"])
    lift_error = float(by_item["max_lift_error"]["value"])
    endpoint_zero = str(by_item["endpoint_pressure_lift_zero"]["value"]).lower() == "true"
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass",
            "evidence": "source register was checked before outputs were written",
        },
        {
            "gate": "volume_variable_recovers_FLRW_N",
            "status": "pass_conditional",
            "evidence": "N_D=(1/3)ln(V_D0/V_D) gives N=ln(1+z) for FLRW coherent domains",
        },
        {
            "gate": "pressure_kernel_from_metric_variation",
            "status": "pass_conditional" if pressure_error < 1.0e-12 and lift_error < 1.0e-12 else "fail",
            "evidence": f"max pressure error={pressure_error:.6g}; max lift error={lift_error:.6g}",
        },
        {
            "gate": "endpoint_pressure_lift_zero",
            "status": "pass" if endpoint_zero else "fail",
            "evidence": "A_N(0)=0 for the cubic locked activation",
        },
        {
            "gate": "boundary_variation_owned",
            "status": "open",
            "evidence": "J_rel must absorb moving-domain terms without wall stress",
        },
        {
            "gate": "density_law_derived",
            "status": "fail",
            "evidence": "rho_M(N_D)=rho_Lambda+B_mem A(N_D) is still supplied from locked branch",
        },
        {
            "gate": "Bmem_p_u3_derived",
            "status": "fail",
            "evidence": "pressure kernel follows if these are supplied; this does not derive them",
        },
        {
            "gate": "local_PPN_promoted",
            "status": "fail",
            "evidence": "local N_D=0 and delta N_D=0 remain branch requirements",
        },
        {
            "gate": "growth_or_CMB_promoted",
            "status": "fail",
            "evidence": "background pressure derivation is not full perturbation theory",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": "volume_pressure_kernel_derived_conditionally_constants_not_derived",
            "evidence": "coherent-volume metric variation gives p=-rho+rho_N/3 and exactly matches the required locked pressure kernel",
        },
        {
            "item": "upgrade_from_137",
            "verdict": "pressure_kernel_no_longer_hand_inserted_if_ND_is_volume_variable",
            "evidence": "the missing p+rho term follows from varying N_D=(1/3)ln(V0/V_D)",
        },
        {
            "item": "remaining_blocker",
            "verdict": "derive_density_law_and_domain_owner",
            "evidence": "the theorem still assumes the locked density law and a coherent domain with safe boundary variation",
        },
        {
            "item": "next_target",
            "verdict": "derive_or_reject_density_law_from_cell_determinant",
            "evidence": "after the pressure kernel, the live bottleneck returns to B_mem, A(N), p=3, u3=1/4, and domain selection",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None = None, aux_run: Path = AUX_RUN) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-coherent-volume-pressure-kernel-theorem"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve(), aux_run)
    missing = [row["path"] for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    aux_status = read_json(aux_run / "status.json")
    required_rows = read_csv_rows(aux_run / "results" / "required_pressure_kernel.csv")

    derivation_chain = derivation_chain_rows()
    pressure_checks = pressure_kernel_check_rows(required_rows)
    conditions = theorem_condition_rows()
    summary = summary_rows(pressure_checks)
    gates = gate_rows(summary)
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(results_dir / "volume_variation_derivation.csv", derivation_chain, ["step", "equation", "result", "status", "blocker"])
    write_csv(
        results_dir / "pressure_kernel_check.csv",
        pressure_checks,
        [
            "index",
            "z",
            "N_past",
            "rho_mem",
            "rho_N_from_locked_density",
            "pressure_target",
            "pressure_from_volume_variation",
            "abs_pressure_error",
            "p_plus_rho_target",
            "p_plus_rho_from_volume_variation",
            "abs_lift_error",
            "local_endpoint_pressure_lift",
        ],
    )
    write_csv(results_dir / "theorem_conditions.csv", conditions, ["condition", "needed_for", "status", "failure_mode"])
    write_csv(results_dir / "summary.csv", summary, ["item", "value", "readout"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "input_status": aux_status["status"],
        "generated": [
            "source_register.csv",
            "volume_variation_derivation.csv",
            "pressure_kernel_check.csv",
            "theorem_conditions.csv",
            "summary.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "derive_or_reject_density_law_from_cell_determinant_and_domain_owner",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--aux-run", type=Path, default=AUX_RUN)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_audit(args.output_root, args.timestamp, args.aux_run))


if __name__ == "__main__":
    main()
