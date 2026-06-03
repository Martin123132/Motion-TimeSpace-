#!/usr/bin/env python3
"""Attempt to derive/fence the P_top and P_MTS support projectors for J_C."""

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

STATUS = "Ptop_conditionally_relative_cohomology_PMTS_requires_parent_sector_charge"
CLAIM_CEILING = "support_projector_contract_only_no_local_GR_PPN_Bmem_or_unification_promotion"


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
        WORK_DIR / "251-N5-boundary-projector-parent-owner-or-modified-exterior-branch.md",
        WORK_DIR / "252-topological-projector-parent-action-skeleton.md",
        WORK_DIR / "253-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure.md",
        WORK_DIR / "271-parent-no-Cperp-action-or-closure.md",
        WORK_DIR / "272-quotient-configuration-principle-from-topological-projector.md",
        WORK_DIR / "323-S3-sector-label-combined-gate.md",
        WORK_DIR / "324-CD-activity-kernel-commutation-gate.md",
        WORK_DIR / "327-JC-parent-current-bridge-gate.md",
        SCRIPT_DIR / "JC_parent_current_bridge_gate.py",
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


def basis_rows() -> list[dict[str, Any]]:
    return [
        {
            "basis_index": 0,
            "state": "stationary_local_exact",
            "sector": "ordinary",
            "relative_class": "exact",
            "description": "Stationary compact local residual; should be killed by topological quotient.",
        },
        {
            "basis_index": 1,
            "state": "tracefree_shear_exact",
            "sector": "ordinary",
            "relative_class": "exact",
            "description": "Tracefree local shear residual; should be killed after coherent projection/topological quotient.",
        },
        {
            "basis_index": 2,
            "state": "ordinary_coherent_exact",
            "sector": "ordinary",
            "relative_class": "exact",
            "description": "Ordinary coherent IR relative bath; the dangerous singlet leakage if exactness is not imposed.",
        },
        {
            "basis_index": 3,
            "state": "MTS_FLRW_top_class",
            "sector": "MTS",
            "relative_class": "top",
            "description": "Desired coherent FLRW memory class.",
        },
        {
            "basis_index": 4,
            "state": "edge_horizon_top_class",
            "sector": "edge",
            "relative_class": "top",
            "description": "Non-MTS topological/edge class that P_top alone cannot reject.",
        },
    ]


def projector_matrix(diagonal: list[float]) -> np.ndarray:
    return np.diag(np.asarray(diagonal, dtype=float))


def projector_rows() -> list[dict[str, Any]]:
    p_top = projector_matrix([0, 0, 0, 1, 1])
    p_mts = projector_matrix([0, 0, 0, 1, 0])
    p_support = p_mts @ p_top
    p_bad_s3_like = projector_matrix([0, 0, 1, 1, 1])
    projectors = [
        ("P_top", "relative cohomology projector onto non-exact domain classes", p_top),
        ("P_MTS", "spectral projector onto the MTS sector if parent charge is supplied", p_mts),
        ("P_MTS_P_top", "repaired support projector for J_C", p_support),
        ("P_singlet_like_without_sector", "coherent/singlet-like selector without support charge", p_bad_s3_like),
    ]
    rows: list[dict[str, Any]] = []
    for label, meaning, matrix in projectors:
        rows.append(
            {
                "projector": label,
                "meaning": meaning,
                "trace": float(np.trace(matrix)),
                "rank": int(np.linalg.matrix_rank(matrix)),
                "idempotence_error": float(np.linalg.norm(matrix @ matrix - matrix)),
                "status": "pass" if np.linalg.norm(matrix @ matrix - matrix) < 1e-12 else "fail",
            }
        )
    return rows


def support_action_rows() -> list[dict[str, Any]]:
    basis = basis_rows()
    p_top = projector_matrix([0, 0, 0, 1, 1])
    p_mts = projector_matrix([0, 0, 0, 1, 0])
    p_support = p_mts @ p_top
    p_bad_s3_like = projector_matrix([0, 0, 1, 1, 1])
    rows: list[dict[str, Any]] = []
    for item in basis:
        vector = np.zeros(5)
        vector[int(item["basis_index"])] = 1.0
        row = dict(item)
        for label, matrix in [
            ("P_top", p_top),
            ("P_MTS", p_mts),
            ("P_MTS_P_top", p_support),
            ("P_singlet_like_without_sector", p_bad_s3_like),
        ]:
            row[label] = float(np.linalg.norm(matrix @ vector))
        row["desired_support"] = 1.0 if item["state"] == "MTS_FLRW_top_class" else 0.0
        row["P_top_leaks"] = row["P_top"] != row["desired_support"] and row["P_top"] != 0.0
        row["P_MTS_P_top_leaks"] = row["P_MTS_P_top"] != row["desired_support"]
        rows.append(row)
    return rows


def charge_rows() -> list[dict[str, Any]]:
    charges = {
        "Q_good_sector_charge": [0, 0, 0, 1, 2],
        "Q_degenerate_top_charge": [0, 0, 0, 1, 1],
        "Q_singlet_like_charge": [0, 0, 1, 1, 1],
    }
    rows: list[dict[str, Any]] = []
    for label, eigenvalues in charges.items():
        eig = np.asarray(eigenvalues, dtype=float)
        mts_value = eig[3]
        degeneracies = [index for index, value in enumerate(eig) if index != 3 and abs(value - mts_value) < 1e-12]
        spectral_projector_possible = len(degeneracies) == 0
        rows.append(
            {
                "charge_operator": label,
                "eigenvalues_by_basis": ";".join(str(v) for v in eigenvalues),
                "MTS_eigenvalue": mts_value,
                "degenerate_with_MTS_basis_indices": ";".join(str(i) for i in degeneracies) if degeneracies else "none",
                "spectral_PMTS_possible": spectral_projector_possible,
                "status": "pass" if spectral_projector_possible else "fail",
                "meaning": "MTS is a unique charge sector" if spectral_projector_possible else "charge cannot distinguish MTS from leakage states",
            }
        )
    return rows


def commutation_rows() -> list[dict[str, Any]]:
    p_support = projector_matrix([0, 0, 0, 1, 0])
    k_good = np.diag([0.2, 0.2, 0.3, 1.0, 0.4])
    k_ordinary_mix = k_good.copy()
    k_ordinary_mix[2, 3] = k_ordinary_mix[3, 2] = 0.15
    k_edge_mix = k_good.copy()
    k_edge_mix[3, 4] = k_edge_mix[4, 3] = 0.15
    rows: list[dict[str, Any]] = []
    for label, kernel in [
        ("K_sector_block_or_functional", k_good),
        ("K_ordinary_MTS_mixing", k_ordinary_mix),
        ("K_edge_MTS_mixing", k_edge_mix),
    ]:
        commutator = kernel @ p_support - p_support @ kernel
        norm = float(np.linalg.norm(commutator))
        rows.append(
            {
                "kernel": label,
                "commutator_norm_with_support": norm,
                "status": "pass" if norm < 1e-12 else "fail",
                "meaning": "support is preserved" if norm < 1e-12 else "support leaks through kernel mixing",
            }
        )
    return rows


def theorem_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "C1",
            "requirement": "P_top is a metric-independent relative cohomology/chain projector.",
            "current_status": "conditional_parent_skeleton_exists",
            "blocks_promotion": False,
        },
        {
            "clause": "C2",
            "requirement": "Local ordinary residuals are relative-exact representatives.",
            "current_status": "not_parent_derived_for_full_C_sector",
            "blocks_promotion": True,
        },
        {
            "clause": "C3",
            "requirement": "Local boundary primitive vanishes for stationary compact domains.",
            "current_status": "boundary_condition_contract_not_parent_derived",
            "blocks_promotion": True,
        },
        {
            "clause": "C4",
            "requirement": "FLRW memory is a non-exact domain class retained by P_top.",
            "current_status": "conditional_shape_bridge",
            "blocks_promotion": False,
        },
        {
            "clause": "C5",
            "requirement": "P_MTS follows as a spectral projector of a parent conserved sector charge.",
            "current_status": "conditional_schema_only",
            "blocks_promotion": True,
        },
        {
            "clause": "C6",
            "requirement": "The sector charge distinguishes MTS top class from edge/horizon top classes.",
            "current_status": "not_parent_derived",
            "blocks_promotion": True,
        },
        {
            "clause": "C7",
            "requirement": "The parent kernel commutes with the full support projector.",
            "current_status": "conditional_only_if_sector_block_or_functional",
            "blocks_promotion": True,
        },
        {
            "clause": "C8",
            "requirement": "The support projector also yields B_mem=2/27 and kappa_mem=1.",
            "current_status": "not_parent_derived",
            "blocks_promotion": True,
        },
        {
            "clause": "C9",
            "requirement": "The resulting local PPN residual vector is zero.",
            "current_status": "not_derived",
            "blocks_promotion": True,
        },
        {
            "clause": "C10",
            "requirement": "No additional by-hand sector label is needed.",
            "current_status": "failed_without_parent_sector_charge",
            "blocks_promotion": True,
        },
    ]


def gate_rows(support_rows: list[dict[str, Any]], charge_rows_: list[dict[str, Any]], commutation: list[dict[str, Any]], clauses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_state = {row["state"]: row for row in support_rows}
    by_charge = {row["charge_operator"]: row for row in charge_rows_}
    by_kernel = {row["kernel"]: row for row in commutation}
    by_clause = {row["clause"]: row for row in clauses}
    gates = [
        ("source_paths_exist", "pass", "All required checkpoint/script paths exist."),
        ("P_top_idempotent_relative_projector", "pass", "P_top^2=P_top in toy relative complex."),
        ("P_top_kills_exact_local_states", "pass" if all(float(by_state[name]["P_top"]) == 0.0 for name in ["stationary_local_exact", "tracefree_shear_exact", "ordinary_coherent_exact"]) else "fail", "exact local representatives have zero P_top support."),
        ("P_top_retains_FLRW_memory", "pass" if float(by_state["MTS_FLRW_top_class"]["P_top"]) == 1.0 else "fail", by_state["MTS_FLRW_top_class"]["P_top"]),
        ("P_top_edge_leak_detected", "pass" if bool(by_state["edge_horizon_top_class"]["P_top_leaks"]) else "fail", by_state["edge_horizon_top_class"]["P_top"]),
        ("PMTS_spectral_projector_possible_if_good_charge_supplied", by_charge["Q_good_sector_charge"]["status"], by_charge["Q_good_sector_charge"]["meaning"]),
        ("PMTS_degenerate_charge_counterexample", "pass" if by_charge["Q_degenerate_top_charge"]["status"] == "fail" else "fail", by_charge["Q_degenerate_top_charge"]["meaning"]),
        ("singlet_like_charge_counterexample", "pass" if by_charge["Q_singlet_like_charge"]["status"] == "fail" else "fail", by_charge["Q_singlet_like_charge"]["meaning"]),
        ("full_support_retains_only_MTS_sample", "pass" if not any(bool(row["P_MTS_P_top_leaks"]) for row in support_rows) else "fail", "P_MTS P_top matches desired toy support."),
        ("kernel_commutes_if_block_functional", by_kernel["K_sector_block_or_functional"]["status"], by_kernel["K_sector_block_or_functional"]["commutator_norm_with_support"]),
        ("kernel_mixing_counterexample", "pass" if by_kernel["K_edge_MTS_mixing"]["status"] == "fail" else "fail", by_kernel["K_edge_MTS_mixing"]["commutator_norm_with_support"]),
        ("local_exactness_parent_derived", "fail", by_clause["C2"]["current_status"]),
        ("boundary_primitive_parent_derived", "fail", by_clause["C3"]["current_status"]),
        ("sector_charge_parent_derived", "fail", by_clause["C6"]["current_status"]),
        ("Bmem_parent_derived", "fail", by_clause["C8"]["current_status"]),
        ("local_PPN_residual_zero_derived", "fail", by_clause["C9"]["current_status"]),
        ("promotion_allowed", "fail", "P_top has a conditional cohomology route; P_MTS still requires a parent sector charge."),
    ]
    return [{"gate": gate, "status": status, "evidence": evidence} for gate, status, evidence in gates]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "decision",
            "verdict": STATUS,
            "evidence": "P_top can be represented as a relative cohomology projector that kills exact local states and keeps domain top classes; P_MTS still requires a nondegenerate parent sector charge.",
        },
        {
            "item": "P_top_status",
            "verdict": "conditional_relative_cohomology_projector",
            "evidence": "Metric-independent topological skeleton plus presymplectic quotient gives a real route, but exactness/boundary primitive for the full C/J_C sector is not yet parent-derived.",
        },
        {
            "item": "P_MTS_status",
            "verdict": "conditional_spectral_projector_not_parent_owned",
            "evidence": "If a conserved sector charge uniquely labels MTS, P_MTS is a spectral idempotent; if the charge is degenerate with ordinary/edge classes, leakage remains.",
        },
        {
            "item": "best_support_expression",
            "verdict": "P_support = P_MTS P_top",
            "evidence": "This kills exact ordinary states and edge top classes in the toy support audit while retaining FLRW MTS memory.",
        },
        {
            "item": "main_failure",
            "verdict": "sector_charge_and_exactness_not_derived",
            "evidence": "No current parent action proves local exactness, vanishing boundary primitive, or a nondegenerate MTS sector charge.",
        },
        {
            "item": "next_target",
            "verdict": "move_to_growth_unless_new_sector_charge_idea_appears",
            "evidence": "The local/projector branch has reached a clean conditional contract; further progress needs a genuinely new parent charge, so empirical growth is the next judge.",
        },
    ]


def run_gate(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-topological-MTS-support-projector-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    missing = [row for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    basis = basis_rows()
    projectors = projector_rows()
    support = support_action_rows()
    charges = charge_rows()
    commutation = commutation_rows()
    clauses = theorem_clause_rows()
    gates = gate_rows(support, charges, commutation, clauses)
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(results_dir / "basis_states.csv", basis, ["basis_index", "state", "sector", "relative_class", "description"])
    write_csv(results_dir / "projector_algebra.csv", projectors, ["projector", "meaning", "trace", "rank", "idempotence_error", "status"])
    write_csv(
        results_dir / "support_action.csv",
        support,
        [
            "basis_index",
            "state",
            "sector",
            "relative_class",
            "description",
            "P_top",
            "P_MTS",
            "P_MTS_P_top",
            "P_singlet_like_without_sector",
            "desired_support",
            "P_top_leaks",
            "P_MTS_P_top_leaks",
        ],
    )
    write_csv(results_dir / "sector_charge_spectral_tests.csv", charges, ["charge_operator", "eigenvalues_by_basis", "MTS_eigenvalue", "degenerate_with_MTS_basis_indices", "spectral_PMTS_possible", "status", "meaning"])
    write_csv(results_dir / "kernel_commutation.csv", commutation, ["kernel", "commutator_norm_with_support", "status", "meaning"])
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
                "basis_states.csv",
                "projector_algebra.csv",
                "support_action.csv",
                "sector_charge_spectral_tests.csv",
                "kernel_commutation.csv",
                "theorem_clauses.csv",
                "gate_results.csv",
                "decision.csv",
            ],
            "next_target": "328-topological-MTS-support-projector-gate.md",
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
