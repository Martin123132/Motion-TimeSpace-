#!/usr/bin/env python3
"""Radial-memory parent-action contract for the locked 2/27 branch."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

STATUS = "radial_memory_kernel_conditional_survival_action_contract_not_parent_derived"
CLAIM_CEILING = "conditional_radial_memory_contract_no_GR_CMB_or_Bmem_promotion"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        Path(__file__).resolve(),
        WORK_DIR / "320-parent-cell-amplitude-theorem-gate.md",
        WORK_DIR / "321-rank-two-screen-projector-gate.md",
        WORK_DIR / "322-S3-singlet-motion-time-projector-gate.md",
        WORK_DIR / "324-CD-activity-kernel-commutation-gate.md",
        WORK_DIR / "325-noCMB-BAO-Hz-pressure-after-projector-fence.md",
        WORK_DIR / "126-Hz-radial-expansion-smoke.md",
        WORK_DIR / "128-BAO-Hz-noCMB-diagnostic.md",
        WORK_DIR / "129-noCMB-radial-robustness-or-growth-route.md",
        SCRIPT_DIR / "cosmo_SN_BAO_closure_runner.py",
        SCRIPT_DIR / "BAO_Hz_noCMB_robustness.py",
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


def singlet_projector() -> np.ndarray:
    return np.ones((3, 3), dtype=float) / 3.0


def screen_projector() -> np.ndarray:
    return np.diag([1.0, 1.0, 0.0])


def projector_rows() -> list[dict[str, Any]]:
    motion_singlet = singlet_projector()
    time_singlet = singlet_projector()
    transverse_screen = screen_projector()
    active_projector = np.kron(np.kron(motion_singlet, time_singlet), transverse_screen)
    bad_spatial_lift = np.kron(np.kron(np.eye(3), np.eye(3)), transverse_screen)
    scalar_trace_lift = np.kron(np.kron(motion_singlet, time_singlet), np.diag([1.0, 0.0, 0.0]))
    candidates = [
        ("P_M_singlet", motion_singlet, 3),
        ("P_T_singlet", time_singlet, 3),
        ("P_screen", transverse_screen, 3),
        ("P_active", active_projector, 27),
        ("bad_spatial_lift", bad_spatial_lift, 27),
        ("scalar_trace_lift", scalar_trace_lift, 27),
    ]
    rows: list[dict[str, Any]] = []
    for label, matrix, dimension in candidates:
        idempotence_error = float(np.linalg.norm(matrix @ matrix - matrix))
        trace = float(np.trace(matrix))
        rank = int(np.linalg.matrix_rank(matrix, tol=1e-10))
        rows.append(
            {
                "object": label,
                "dimension": dimension,
                "trace": trace,
                "rank": rank,
                "normalized_trace": trace / dimension,
                "idempotence_error": idempotence_error,
                "status": "pass" if idempotence_error < 1e-10 else "fail",
            }
        )
    return rows


def activation_rows(scale_u: float = 0.25, amplitude_b: float = 2.0 / 27.0) -> list[dict[str, Any]]:
    cubic_coefficient = scale_u ** -3
    third_derivative = 6.0 * cubic_coefficient
    samples = []
    for log_redshift in [0.0, 0.01, 0.05, 0.25, 1.0]:
        cumulative_hazard = (log_redshift / scale_u) ** 3
        activation = 1.0 - float(np.exp(-cumulative_hazard))
        hazard_rate = 3.0 * log_redshift**2 / scale_u**3
        activation_slope = float(np.exp(-cumulative_hazard)) * hazard_rate
        memory_density = amplitude_b * activation
        memory_pressure = -memory_density + amplitude_b * activation_slope / 3.0
        effective_w = "" if abs(memory_density) < 1e-15 else memory_pressure / memory_density
        samples.append(
            {
                "log_redshift": log_redshift,
                "cumulative_hazard": cumulative_hazard,
                "activation": activation,
                "hazard_rate": hazard_rate,
                "activation_slope": activation_slope,
                "memory_density_over_rhocrit0": memory_density,
                "memory_pressure_over_rhocrit0": memory_pressure,
                "effective_w_if_density_nonzero": effective_w,
            }
        )
    rows = [
        {
            "item": "survival_equation",
            "value": "dA/dy=(1-A)dH/dy",
            "status": "conditional_pass",
            "meaning": "If the parent action supplies a cumulative hazard H(y), the activation follows without fitting a shape function.",
        },
        {
            "item": "cubic_cumulative_hazard",
            "value": "H(y)=(y/u3)^3",
            "status": "conditional_not_parent_derived",
            "meaning": "Cubic hazard gives the locked p=3 kernel, but the parent action still has to derive cubic order.",
        },
        {
            "item": "u3",
            "value": scale_u,
            "status": "closure_not_parent_derived",
            "meaning": "u3=1/4 is the locked branch scale; this artifact does not derive the quarter.",
        },
        {
            "item": "A(0)",
            "value": 0.0,
            "status": "pass",
            "meaning": "No present-epoch offset from the radial memory term.",
        },
        {
            "item": "A_prime(0)",
            "value": 0.0,
            "status": "pass",
            "meaning": "No linear late-time deformation.",
        },
        {
            "item": "A_second(0)",
            "value": 0.0,
            "status": "pass",
            "meaning": "No quadratic late-time deformation.",
        },
        {
            "item": "A_third(0)",
            "value": third_derivative,
            "status": "pass",
            "meaning": "The first nonzero local-in-y term is cubic.",
        },
        {
            "item": "series_leading_term",
            "value": f"A(y)={cubic_coefficient:g} y^3 + O(y^6)",
            "status": "pass",
            "meaning": "For u3=1/4, the leading coefficient is 64.",
        },
        {
            "item": "pressure_limit_y_to_0",
            "value": 0.0,
            "status": "pass",
            "meaning": "The conserved effective pressure is finite at y=0, although w=p/rho is not a useful variable when rho=0.",
        },
        {
            "item": "pressure_limit_y_to_infinity",
            "value": -amplitude_b,
            "status": "pass",
            "meaning": "The memory component tends to a constant-density, w=-1-like asymptote.",
        },
    ]
    for sample in samples:
        rows.append(
            {
                "item": f"sample_y_{sample['log_redshift']}",
                "value": json.dumps(sample, sort_keys=True),
                "status": "diagnostic",
                "meaning": "Numerical activation and conserved-pressure sample.",
            }
        )
    return rows


def theorem_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "C1",
            "requirement": "Parent cell is V_M tensor V_T tensor V_S with dimension 27.",
            "current_status": "conditional_not_parent_derived",
            "blocks_promotion": True,
        },
        {
            "clause": "C2",
            "requirement": "Motion and time/history factors are S3 coherent singlets.",
            "current_status": "conditional_not_parent_derived",
            "blocks_promotion": True,
        },
        {
            "clause": "C3",
            "requirement": "Spatial factor is a parent-owned transverse screen bundle.",
            "current_status": "conditional_not_parent_derived",
            "blocks_promotion": True,
        },
        {
            "clause": "C4",
            "requirement": "Amplitude is normalized cell trace with kappa_mem=1.",
            "current_status": "kappa_not_parent_derived",
            "blocks_promotion": True,
        },
        {
            "clause": "C5",
            "requirement": "Radial activation comes from survival law with H(y)=(y/u3)^3.",
            "current_status": "conditional_kernel_derivation",
            "blocks_promotion": True,
        },
        {
            "clause": "C6",
            "requirement": "u3=1/4 follows from parent no-clock/routing measure.",
            "current_status": "closure_not_parent_derived",
            "blocks_promotion": True,
        },
        {
            "clause": "C7",
            "requirement": "C_D annihilates ordinary coherent local baths while retaining FLRW memory.",
            "current_status": "not_parent_derived",
            "blocks_promotion": True,
        },
        {
            "clause": "C8",
            "requirement": "Boundary kernel obeys [K_boundary,A_D]=0 from the action.",
            "current_status": "not_parent_derived",
            "blocks_promotion": True,
        },
        {
            "clause": "C9",
            "requirement": "Effective stress is Bianchi-compatible after the memory term is added.",
            "current_status": "conditional_pass_if_pressure_included",
            "blocks_promotion": False,
        },
        {
            "clause": "C10",
            "requirement": "Local PPN residual vector is zero without imposing a plateau axiom.",
            "current_status": "not_derived",
            "blocks_promotion": True,
        },
    ]


def gate_rows(projectors: list[dict[str, Any]], clauses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    projector_lookup = {row["object"]: row for row in projectors}
    active = projector_lookup["P_active"]
    bad_lift = projector_lookup["bad_spatial_lift"]
    clause_lookup = {row["clause"]: row for row in clauses}
    gates = [
        ("source_paths_exist", "pass", "All required checkpoint/script paths exist."),
        ("P_active_idempotent", "pass" if float(active["idempotence_error"]) < 1e-10 else "fail", active["idempotence_error"]),
        ("P_active_trace_2", "pass" if abs(float(active["trace"]) - 2.0) < 1e-10 else "fail", active["trace"]),
        ("P_active_normalized_trace_2_over_27", "pass" if abs(float(active["normalized_trace"]) - 2.0 / 27.0) < 1e-10 else "fail", active["normalized_trace"]),
        ("bad_spatial_lift_rejected", "pass" if abs(float(bad_lift["normalized_trace"]) - 2.0 / 3.0) < 1e-10 else "fail", bad_lift["normalized_trace"]),
        ("survival_kernel_double_zero", "pass", "A(0)=A'(0)=A''(0)=0 for p=3."),
        ("effective_pressure_finite", "pass", "p_mem -> 0 at y=0 and p_mem -> -B_mem at large y."),
        ("dim27_parent_derived", "fail", clause_lookup["C1"]["current_status"]),
        ("kappa_mem_parent_derived", "fail", clause_lookup["C4"]["current_status"]),
        ("u3_parent_derived", "fail", clause_lookup["C6"]["current_status"]),
        ("CD_parent_derived", "fail", clause_lookup["C7"]["current_status"]),
        ("kernel_commutation_parent_derived", "fail", clause_lookup["C8"]["current_status"]),
        ("local_PPN_residual_zero_derived", "fail", clause_lookup["C10"]["current_status"]),
        ("promotion_allowed", "fail", "Contract is conditional and closure-level."),
    ]
    return [{"gate": gate, "status": status, "evidence": evidence} for gate, status, evidence in gates]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "decision",
            "verdict": STATUS,
            "evidence": "The radial memory kernel can be written as a survival activation with cubic hazard, but the parent origin of cubic order, u3, kappa, C_D, and local PPN silence is still missing.",
        },
        {
            "item": "derived_piece",
            "verdict": "conditional_survival_kernel_and_trace_amplitude",
            "evidence": "If H(y)=(y/u3)^3 and P_active=P_M_singlet tensor P_T_singlet tensor P_screen, then A=1-exp(-H) and Tr(P_active)/27=2/27.",
        },
        {
            "item": "useful_win",
            "verdict": "double_zero_local_in_y",
            "evidence": "The p=3 kernel has A(0)=A'(0)=A''(0)=0, so the first late-time deformation is cubic.",
        },
        {
            "item": "main_failure",
            "verdict": "parent_action_not_owned",
            "evidence": "No current action derives H(y), u3=1/4, kappa_mem=1, C_D, [K_boundary,A_D]=0, or a zero local PPN residual.",
        },
        {
            "item": "next_target",
            "verdict": "derive_CD_or_test_growth",
            "evidence": "Either find a parent current whose support is C_D and whose cumulative FLRW hazard is cubic, or move to growth as the next external judge.",
        },
    ]


def run_contract(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-radial-memory-parent-action-contract"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    missing = [row for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    projectors = projector_rows()
    activation = activation_rows()
    clauses = theorem_clause_rows()
    gates = gate_rows(projectors, clauses)
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(results_dir / "projector_trace_algebra.csv", projectors, ["object", "dimension", "trace", "rank", "normalized_trace", "idempotence_error", "status"])
    write_csv(results_dir / "activation_kernel.csv", activation, ["item", "value", "status", "meaning"])
    write_csv(results_dir / "theorem_clauses.csv", clauses, ["clause", "requirement", "current_status", "blocks_promotion"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])
    write_json(
        run_dir / "status.json",
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "run_dir": str(run_dir),
            "results_dir": str(results_dir),
            "generated": [
                "source_register.csv",
                "projector_trace_algebra.csv",
                "activation_kernel.csv",
                "theorem_clauses.csv",
                "gate_results.csv",
                "decision.csv",
            ],
            "next_target": "326-radial-memory-parent-action-contract.md",
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
    print(run_contract(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()
