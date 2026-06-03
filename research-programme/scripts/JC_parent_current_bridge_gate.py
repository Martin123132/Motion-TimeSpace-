#!/usr/bin/env python3
"""Bridge gate for a Q-coherent three-form parent current J_C."""

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

STATUS = "JC_Qcoh_derives_FLRW_cubic_hazard_but_not_sector_support_or_local_PPN"
CLAIM_CEILING = "conditional_JC_bridge_no_Bmem_local_GR_PPN_or_unification_promotion"


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
        WORK_DIR / "274-lifted-C-sector-form-holonomy-route.md",
        WORK_DIR / "275-JC-three-form-memory-current-from-Q.md",
        WORK_DIR / "276-coherent-domain-projector-from-parent-variables.md",
        WORK_DIR / "324-CD-activity-kernel-commutation-gate.md",
        WORK_DIR / "325-noCMB-BAO-Hz-pressure-after-projector-fence.md",
        WORK_DIR / "326-radial-memory-parent-action-contract.md",
        SCRIPT_DIR / "JC_three_form_memory_current_from_Q.py",
        SCRIPT_DIR / "coherent_domain_projector_from_parent_variables.py",
        SCRIPT_DIR / "radial_memory_parent_action_contract.py",
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


def q_matrix(coherent_q: float, shear_diag: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> np.ndarray:
    return coherent_q * np.eye(3) + np.diag(shear_diag)


def coherent_projection(q_tensor: np.ndarray) -> np.ndarray:
    coherent_q = float(np.trace(q_tensor) / 3.0)
    return coherent_q * np.eye(3)


def matrix_summary(label: str, q_tensor: np.ndarray) -> dict[str, Any]:
    q_coh = coherent_projection(q_tensor)
    shear = q_tensor - q_coh
    return {
        "state": label,
        "trace_Q": float(np.trace(q_tensor)),
        "coherent_q": float(np.trace(q_coh) / 3.0),
        "tracefree_norm": float(np.linalg.norm(shear)),
        "det_Q": float(np.linalg.det(q_tensor)),
        "det_Qcoh": float(np.linalg.det(q_coh)),
    }


def source_state_rows() -> list[dict[str, Any]]:
    states = [
        {
            "state": "stationary_local_domain",
            "description": "Local stationary domain with no coherent volume-flow class.",
            "sector": "ordinary",
            "relative_class": "exact_local",
            "topological_support": 0.0,
            "mts_support": 0.0,
            "q_tensor": q_matrix(0.0),
        },
        {
            "state": "tracefree_shear_wave",
            "description": "Tracefree local shear/GW-like content.",
            "sector": "ordinary",
            "relative_class": "exact_local",
            "topological_support": 0.0,
            "mts_support": 0.0,
            "q_tensor": q_matrix(0.0, (0.2, -0.1, -0.1)),
        },
        {
            "state": "ordinary_coherent_IR_relative_bath",
            "description": "Ordinary coherent scalar/IR relative bath; the known leakage case.",
            "sector": "ordinary",
            "relative_class": "exact_local",
            "topological_support": 0.0,
            "mts_support": 0.0,
            "q_tensor": q_matrix(0.2),
        },
        {
            "state": "MTS_FLRW_memory_class",
            "description": "Coherent FLRW memory class with N/u3=1 in the sample.",
            "sector": "MTS",
            "relative_class": "domain_top_class",
            "topological_support": 1.0,
            "mts_support": 1.0,
            "q_tensor": q_matrix(1.0),
        },
        {
            "state": "edge_horizon_coherent_class",
            "description": "Non-MTS coherent boundary/horizon class.",
            "sector": "edge",
            "relative_class": "domain_top_class",
            "topological_support": 1.0,
            "mts_support": 0.0,
            "q_tensor": q_matrix(0.8),
        },
    ]
    rows: list[dict[str, Any]] = []
    for state in states:
        summary = matrix_summary(state["state"], state["q_tensor"])
        base_current = summary["det_Qcoh"]
        top_current = state["topological_support"] * base_current
        mts_current = state["mts_support"] * top_current
        rows.append(
            {
                "state": state["state"],
                "description": state["description"],
                "sector": state["sector"],
                "relative_class": state["relative_class"],
                "topological_support": state["topological_support"],
                "mts_support": state["mts_support"],
                "trace_Q": summary["trace_Q"],
                "coherent_q": summary["coherent_q"],
                "tracefree_norm": summary["tracefree_norm"],
                "det_Q": summary["det_Q"],
                "det_Qcoh": summary["det_Qcoh"],
                "J_Qcoh": base_current,
                "J_top": top_current,
                "J_MTS": mts_current,
                "base_leaks": base_current != 0.0 and state["sector"] != "MTS",
                "top_leaks": top_current != 0.0 and state["sector"] != "MTS",
                "mts_leaks": mts_current != 0.0 and state["sector"] != "MTS",
            }
        )
    return rows


def flrw_kernel_rows(u3: float = 0.25) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for y in [0.0, 0.01, 0.05, 0.25, 1.0]:
        q = y / u3
        q_tensor = q_matrix(q)
        h_from_jc = float(np.linalg.det(coherent_projection(q_tensor)))
        expected_h = (y / u3) ** 3
        activation = 1.0 - float(np.exp(-h_from_jc))
        rows.append(
            {
                "y_ln1pz": y,
                "u3": u3,
                "q_N_over_u3": q,
                "integral_JC": h_from_jc,
                "expected_cubic_hazard": expected_h,
                "hazard_error": h_from_jc - expected_h,
                "activation": activation,
            }
        )
    return rows


def candidate_rows(states: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates = [
        ("J_Qcoh", "det(P_coh[Q]) Omega_D/V_D", "owns cubic hazard but leaks ordinary coherent and edge classes"),
        ("J_top", "P_top det(P_coh[Q]) Omega_D/V_D", "kills exact local ordinary baths if relative exactness is parent-owned; leaks non-MTS top classes"),
        ("J_MTS", "P_MTS P_top det(P_coh[Q]) Omega_D/V_D", "has the desired support if P_MTS and P_top are supplied"),
    ]
    rows: list[dict[str, Any]] = []
    for key, formula, comment in candidates:
        active_states = [row["state"] for row in states if float(row[key]) != 0.0]
        leakage_states = [row["state"] for row in states if row["sector"] != "MTS" and float(row[key]) != 0.0]
        flrw_survives = any(row["state"] == "MTS_FLRW_memory_class" and float(row[key]) != 0.0 for row in states)
        if leakage_states:
            status = "support_leakage"
        elif flrw_survives:
            status = "conditional_support_pass"
        else:
            status = "kills_FLRW"
        rows.append(
            {
                "candidate": key,
                "formula": formula,
                "active_states": ";".join(active_states) if active_states else "none",
                "leakage_states": ";".join(leakage_states) if leakage_states else "none",
                "FLRW_survives": flrw_survives,
                "status": status,
                "comment": comment,
            }
        )
    return rows


def commutation_rows() -> list[dict[str, Any]]:
    support = np.diag([0.0, 0.0, 0.0, 1.0, 0.0])
    functional_kernel = 2.0 * support + 0.5 * (np.eye(5) - support)
    ordinary_mts_mixing = functional_kernel.copy()
    ordinary_mts_mixing[2, 3] = ordinary_mts_mixing[3, 2] = 0.2
    edge_mts_mixing = functional_kernel.copy()
    edge_mts_mixing[3, 4] = edge_mts_mixing[4, 3] = 0.2
    kernels = [
        ("K_functional_of_A_D", functional_kernel),
        ("K_ordinary_MTS_mixing", ordinary_mts_mixing),
        ("K_edge_MTS_mixing", edge_mts_mixing),
    ]
    rows: list[dict[str, Any]] = []
    for label, kernel in kernels:
        commutator = kernel @ support - support @ kernel
        rows.append(
            {
                "kernel": label,
                "commutator_norm": float(np.linalg.norm(commutator)),
                "status": "pass" if np.linalg.norm(commutator) < 1e-12 else "fail",
                "meaning": "commutes with supplied A_D" if np.linalg.norm(commutator) < 1e-12 else "mixes support with non-support",
            }
        )
    return rows


def theorem_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "C1",
            "requirement": "Construct J_C from fixed-domain Q_coh rather than adding a new repair field.",
            "current_status": "conditional_pass",
            "blocks_promotion": False,
        },
        {
            "clause": "C2",
            "requirement": "FLRW projection gives integral_D J_C=(N/u3)^3.",
            "current_status": "conditional_pass",
            "blocks_promotion": False,
        },
        {
            "clause": "C3",
            "requirement": "Tracefree local shear does not enter J_C.",
            "current_status": "conditional_pass_for_Pcoh",
            "blocks_promotion": False,
        },
        {
            "clause": "C4",
            "requirement": "Local ordinary coherent baths are exact and killed by P_top.",
            "current_status": "relative_exactness_not_parent_derived",
            "blocks_promotion": True,
        },
        {
            "clause": "C5",
            "requirement": "Non-MTS top/edge classes are killed without an inserted sector label.",
            "current_status": "fail_without_P_MTS",
            "blocks_promotion": True,
        },
        {
            "clause": "C6",
            "requirement": "P_MTS or equivalent channel support is derived from parent variables.",
            "current_status": "not_parent_derived",
            "blocks_promotion": True,
        },
        {
            "clause": "C7",
            "requirement": "u3=1/4 follows from the same parent current/measure.",
            "current_status": "not_parent_derived",
            "blocks_promotion": True,
        },
        {
            "clause": "C8",
            "requirement": "B_mem=2/27 and kappa_mem=1 follow from the same parent action.",
            "current_status": "not_parent_derived",
            "blocks_promotion": True,
        },
        {
            "clause": "C9",
            "requirement": "[K_boundary,A_D]=0 follows from the parent boundary kernel.",
            "current_status": "conditional_only_if_K_functional_of_A_D",
            "blocks_promotion": True,
        },
        {
            "clause": "C10",
            "requirement": "Local PPN residual vector is zero without a plateau axiom.",
            "current_status": "not_derived",
            "blocks_promotion": True,
        },
    ]


def gate_rows(states: list[dict[str, Any]], kernels: list[dict[str, Any]], clauses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_state = {row["state"]: row for row in states}
    by_kernel = {row["kernel"]: row for row in kernels}
    by_clause = {row["clause"]: row for row in clauses}
    gates = [
        ("source_paths_exist", "pass", "All required checkpoint/script paths exist."),
        ("JC_constructed_from_Qcoh", "pass", by_clause["C1"]["current_status"]),
        ("FLRW_cubic_hazard", "pass" if float(by_state["MTS_FLRW_memory_class"]["J_Qcoh"]) == 1.0 else "fail", by_state["MTS_FLRW_memory_class"]["J_Qcoh"]),
        ("tracefree_shear_killed_by_Qcoh", "pass" if float(by_state["tracefree_shear_wave"]["J_Qcoh"]) == 0.0 else "fail", by_state["tracefree_shear_wave"]["J_Qcoh"]),
        ("stationary_local_killed", "pass" if float(by_state["stationary_local_domain"]["J_Qcoh"]) == 0.0 else "fail", by_state["stationary_local_domain"]["J_Qcoh"]),
        ("ordinary_coherent_leak_detected_in_base_JQcoh", "pass" if by_state["ordinary_coherent_IR_relative_bath"]["base_leaks"] else "fail", by_state["ordinary_coherent_IR_relative_bath"]["J_Qcoh"]),
        ("ordinary_exact_bath_killed_if_Ptop_supplied", "pass" if float(by_state["ordinary_coherent_IR_relative_bath"]["J_top"]) == 0.0 else "fail", by_state["ordinary_coherent_IR_relative_bath"]["J_top"]),
        ("edge_top_class_leak_detected_without_PMTS", "pass" if by_state["edge_horizon_coherent_class"]["top_leaks"] else "fail", by_state["edge_horizon_coherent_class"]["J_top"]),
        ("PMTS_repaired_support_passes_if_supplied", "pass" if not any(row["mts_leaks"] for row in states) and float(by_state["MTS_FLRW_memory_class"]["J_MTS"]) != 0.0 else "fail", "J_MTS retains only MTS sample."),
        ("K_functional_commutes", by_kernel["K_functional_of_A_D"]["status"], by_kernel["K_functional_of_A_D"]["commutator_norm"]),
        ("generic_kernel_mixing_counterexample", "pass" if by_kernel["K_ordinary_MTS_mixing"]["status"] == "fail" else "fail", by_kernel["K_ordinary_MTS_mixing"]["commutator_norm"]),
        ("relative_exactness_parent_derived", "fail", by_clause["C4"]["current_status"]),
        ("PMTS_parent_derived", "fail", by_clause["C6"]["current_status"]),
        ("u3_parent_derived", "fail", by_clause["C7"]["current_status"]),
        ("Bmem_parent_derived", "fail", by_clause["C8"]["current_status"]),
        ("local_PPN_residual_zero_derived", "fail", by_clause["C10"]["current_status"]),
        ("promotion_allowed", "fail", "J_C owns a conditional cubic-hazard route, not the full local/sector/amplitude theorem."),
    ]
    return [{"gate": gate, "status": status, "evidence": evidence} for gate, status, evidence in gates]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "decision",
            "verdict": STATUS,
            "evidence": "Q_coh three-form J_C conditionally derives the FLRW cubic hazard, but support still needs relative exactness plus an MTS/topological sector selector.",
        },
        {
            "item": "best_candidate",
            "verdict": "J_MTS = P_MTS P_top det(P_coh[Q]) Omega_D/V_D",
            "evidence": "This is the first compact expression that retains FLRW memory, kills exact ordinary local baths, and rejects edge/non-MTS classes in the toy support audit.",
        },
        {
            "item": "real_derivation_gain",
            "verdict": "p_equals_3_from_spatial_determinant",
            "evidence": "For FLRW Q_coh=(N/u3)I, integral_D J_C=det(Q_coh)=(N/u3)^3.",
        },
        {
            "item": "main_failure",
            "verdict": "support_projectors_not_parent_owned",
            "evidence": "P_top/relative exactness and P_MTS are still required; J_Qcoh alone leaks ordinary coherent baths and J_top alone leaks edge/top classes.",
        },
        {
            "item": "claim_ceiling",
            "verdict": "conditional_JC_bridge_no_promotion",
            "evidence": "No derivation of u3=1/4, B_mem=2/27, kappa_mem=1, kernel commutation, or zero local PPN residual.",
        },
        {
            "item": "next_target",
            "verdict": "derive_Ptop_PMTS_or_move_to_growth",
            "evidence": "A further derivation must show relative exactness and MTS sector support from the parent action; otherwise the empirical growth route should be the next judge.",
        },
    ]


def run_gate(output_root: Path, timestamp: str | None = None) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-JC-parent-current-bridge-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    missing = [row for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    states = source_state_rows()
    kernel = flrw_kernel_rows()
    candidates = candidate_rows(states)
    commutation = commutation_rows()
    clauses = theorem_clause_rows()
    gates = gate_rows(states, commutation, clauses)
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(
        results_dir / "source_state_support.csv",
        states,
        [
            "state",
            "description",
            "sector",
            "relative_class",
            "topological_support",
            "mts_support",
            "trace_Q",
            "coherent_q",
            "tracefree_norm",
            "det_Q",
            "det_Qcoh",
            "J_Qcoh",
            "J_top",
            "J_MTS",
            "base_leaks",
            "top_leaks",
            "mts_leaks",
        ],
    )
    write_csv(results_dir / "FLRW_kernel_projection.csv", kernel, ["y_ln1pz", "u3", "q_N_over_u3", "integral_JC", "expected_cubic_hazard", "hazard_error", "activation"])
    write_csv(results_dir / "candidate_current_comparison.csv", candidates, ["candidate", "formula", "active_states", "leakage_states", "FLRW_survives", "status", "comment"])
    write_csv(results_dir / "kernel_commutation.csv", commutation, ["kernel", "commutator_norm", "status", "meaning"])
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
                "source_state_support.csv",
                "FLRW_kernel_projection.csv",
                "candidate_current_comparison.csv",
                "kernel_commutation.csv",
                "theorem_clauses.csv",
                "gate_results.csv",
                "decision.csv",
            ],
            "next_target": "327-JC-parent-current-bridge-gate.md",
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
