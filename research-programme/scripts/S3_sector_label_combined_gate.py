from __future__ import annotations

import argparse
import csv
import itertools
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "S3-sector-label-combined-gate"
STATUS = "S3_singlet_block_structure_conditional_SD_still_independent"
CLAIM_CEILING = "conditional_S3_block_and_SD_support_no_local_GR_or_Bmem_promotion"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def pass_fail(value: bool) -> str:
    return "pass" if value else "fail"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    sources = [
        (script_path, "this combined S3 and sector-label gate"),
        (ROOT / "310-ordinary-MTS-sector-split-attempt.md", "ordinary/MTS sector split theorem target"),
        (ROOT / "311-sector-label-SD-origin-attempt.md", "spectral-support S_D construction"),
        (ROOT / "321-rank-two-screen-projector-gate.md", "rank-two screen projector gate"),
        (ROOT / "322-S3-singlet-motion-time-projector-gate.md", "S3 singlet motion/time projector gate"),
        (ROOT / "scripts" / "sector_label_SD_origin_attempt.py", "S_D predecessor script"),
        (ROOT / "scripts" / "singlet_motion_time_projector_gate.py", "S3 singlet predecessor script"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": yes_no(path.exists()),
            "bytes": path.stat().st_size if path.exists() else 0,
        }
        for path, role in sources
    ]


def permutation_matrix(permutation: tuple[int, int, int]) -> np.ndarray:
    matrix = np.zeros((3, 3), dtype=float)
    for column, row in enumerate(permutation):
        matrix[row, column] = 1.0
    return matrix


def s3_group() -> list[np.ndarray]:
    return [permutation_matrix(permutation) for permutation in itertools.permutations((0, 1, 2))]


def p_singlet() -> np.ndarray:
    group = s3_group()
    return sum(group) / len(group)


def rank(matrix: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(matrix, tol=1.0e-10))


def norm(matrix: np.ndarray) -> float:
    return float(np.linalg.norm(matrix))


def max_commutator_error(matrix: np.ndarray, group: list[np.ndarray]) -> float:
    return float(max(np.linalg.norm(matrix @ g - g @ matrix) for g in group))


def S3_kernel_rows() -> list[dict[str, Any]]:
    group = s3_group()
    ps = p_singlet()
    pd = np.eye(3) - ps
    k_invariant = 2.0 * ps + 5.0 * pd
    k_degenerate = 3.0 * ps + 3.0 * pd
    k_breaking = np.asarray([[1.0, 0.25, 0.0], [0.25, 2.0, 0.1], [0.0, 0.1, 4.0]])
    rows = []
    for name, kernel in [
        ("S3_invariant_non_degenerate", k_invariant),
        ("S3_invariant_degenerate", k_degenerate),
        ("S3_breaking_generic", k_breaking),
    ]:
        rows.append(
            {
                "kernel": name,
                "commutator_error": max_commutator_error(kernel, group),
                "singlet_doublet_cross_norm": norm(ps @ kernel @ pd) + norm(pd @ kernel @ ps),
                "singlet_eigenvalue": float(np.trace(ps @ kernel @ ps) / max(float(np.trace(ps)), 1.0e-12)),
                "doublet_trace_average": float(np.trace(pd @ kernel @ pd) / max(float(np.trace(pd)), 1.0e-12)),
                "readout": "block_diagonal_by_S3" if max_commutator_error(kernel, group) < 1.0e-12 else "S3_broken_cross_terms_allowed",
            }
        )
    return rows


def singlet_leakage_rows() -> list[dict[str, Any]]:
    ps = p_singlet()
    pd = np.eye(3) - ps
    vectors = {
        "FLRW_MTS_equal_memory": np.asarray([1.0, 1.0, 1.0]),
        "ordinary_isotropic_EM_bath": np.asarray([2.0, 2.0, 2.0]),
        "ordinary_isotropic_thermal_bath": np.asarray([0.4, 0.4, 0.4]),
        "anisotropic_local_shear": np.asarray([1.0, -1.0, 0.0]),
        "generic_local_environment": np.asarray([1.0, 2.0, 3.0]),
    }
    rows = []
    for label, vector in vectors.items():
        singlet = ps @ vector
        doublet = pd @ vector
        rows.append(
            {
                "source": label,
                "vector": "[" + ",".join(f"{float(value):.12g}" for value in vector) + "]",
                "singlet_norm": float(np.linalg.norm(singlet)),
                "doublet_norm": float(np.linalg.norm(doublet)),
                "pure_singlet": float(np.linalg.norm(doublet)) < 1.0e-12,
                "MTS_sector_by_S3_alone": float(np.linalg.norm(singlet)) > 1.0e-12,
                "readout": "danger_ordinary_can_be_singlet" if label.startswith("ordinary") else ("MTS_target" if label.startswith("FLRW") else "not_pure_singlet"),
            }
        )
    return rows


def sector_label_rows() -> list[dict[str, Any]]:
    ps = p_singlet()
    sector_identity = np.eye(2)
    mts_sector = np.diag([0.0, 1.0])
    ordinary_sector = np.diag([1.0, 0.0])
    a_d = np.kron(mts_sector, ps)
    s_d = a_d.copy()
    k_cell = 2.0 * ps + 5.0 * (np.eye(3) - ps)
    k_good = np.kron(sector_identity, k_cell)
    sector_mix = np.asarray([[0.0, 1.0], [1.0, 0.0]])
    k_bad = k_good + 0.2 * np.kron(sector_mix, ps)
    p_ord = np.kron(ordinary_sector, np.eye(3))
    p_mts = np.kron(mts_sector, np.eye(3))
    rows = []
    for name, kernel in [
        ("sector_block_kernel", k_good),
        ("sector_mixing_kernel", k_bad),
    ]:
        rows.append(
            {
                "kernel": name,
                "A_D_positive": bool(np.all(np.linalg.eigvalsh(a_d) >= -1.0e-12)),
                "S_D_idempotence_error": norm(s_d @ s_d - s_d),
                "commutator_with_S_D": norm(kernel @ s_d - s_d @ kernel),
                "ordinary_MTS_cross_norm": norm(p_ord @ kernel @ p_mts) + norm(p_mts @ kernel @ p_ord),
                "readout": "sector_split_safe_if_parent_owned" if norm(kernel @ s_d - s_d @ kernel) < 1.0e-12 else "sector_mixing_reappears",
            }
        )
    return rows


def theorem_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "T1_S3_cell_symmetry",
            "needed_statement": "K_cell commutes with S3_M x S3_T on the parent cell sectors",
            "status": "conditional",
            "evidence": "if imposed, singlet/doublet cross terms vanish by block decomposition",
        },
        {
            "clause": "T2_S3_singlet_not_sector_label",
            "needed_statement": "S3 singlet alone cannot define MTS sector because ordinary isotropic baths can also be singlets",
            "status": "pass_no_go",
            "evidence": "ordinary isotropic EM/thermal toy sources project as pure singlets",
        },
        {
            "clause": "T3_SD_support_label",
            "needed_statement": "S_D = support(A_D), A_D=C_D^dagger C_D, separates H_ord from H_MTS",
            "status": "conditional",
            "evidence": "support projector is threshold-free if C_D and inner product are parent-owned",
        },
        {
            "clause": "T4_parent_CD",
            "needed_statement": "parent action derives C_D=P_rel P_IR P_coh or an equivalent MTS activity map",
            "status": "not_derived",
            "evidence": "checkpoint 311 keeps C_D as a contract",
        },
        {
            "clause": "T5_kernel_commutation",
            "needed_statement": "[K_boundary,A_D]=0 or [K_boundary,S_D]=0 follows from parent action",
            "status": "not_derived",
            "evidence": "toy sector-mixing kernel shows generic kernels can mix ordinary and MTS singlet sectors",
        },
        {
            "clause": "T6_amplitude_completion",
            "needed_statement": "S3 singlet, S_D, screen bundle, local silence, and kappa_mem=1 are all parent-derived",
            "status": "not_derived",
            "evidence": "rank-one/rank-two algebra exists conditionally, but sector and kappa gates remain open",
        },
    ]


def gate_rows(
    sources: list[dict[str, Any]],
    kernel_rows: list[dict[str, Any]],
    leakage_rows: list[dict[str, Any]],
    sector_rows: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in sources)
    kernels = {row["kernel"]: row for row in kernel_rows}
    leakage = {row["source"]: row for row in leakage_rows}
    sectors = {row["kernel"]: row for row in sector_rows}
    clause = {row["clause"]: row for row in clauses}
    gates = [
        ("source_paths_exist", sources_ok, "all cited predecessor checkpoints and scripts exist"),
        ("S3_invariant_kernel_block_diagonal", kernels["S3_invariant_non_degenerate"]["readout"] == "block_diagonal_by_S3", "S3-invariant kernels have zero singlet/doublet cross block"),
        ("S3_breaking_kernel_allows_cross_terms", kernels["S3_breaking_generic"]["readout"] == "S3_broken_cross_terms_allowed", "generic S3-breaking kernel allows singlet/doublet cross terms"),
        ("ordinary_coherent_bath_singlet_leakage", leakage["ordinary_isotropic_EM_bath"]["pure_singlet"] == "True" or leakage["ordinary_isotropic_EM_bath"]["pure_singlet"] is True, "ordinary isotropic bath can be pure S3 singlet"),
        ("S3_singlet_not_SD", clause["T2_S3_singlet_not_sector_label"]["status"] == "pass_no_go", "S3 singlet cannot replace the MTS sector label"),
        ("SD_support_label_constructed", sectors["sector_block_kernel"]["A_D_positive"] == "True" or sectors["sector_block_kernel"]["A_D_positive"] is True, "A_D positive and S_D support projector can be written"),
        ("block_kernel_safe_if_commuting", sectors["sector_block_kernel"]["readout"] == "sector_split_safe_if_parent_owned", "commuting/block kernel has zero ordinary/MTS cross block"),
        ("sector_mixing_counterexample", sectors["sector_mixing_kernel"]["readout"] == "sector_mixing_reappears", "generic sector-mixing kernel violates the split"),
        ("parent_CD_derived", clause["T4_parent_CD"]["status"] == "pass", "C_D remains contract-level"),
        ("parent_kernel_commutation_derived", clause["T5_kernel_commutation"]["status"] == "pass", "[K_boundary,A_D]=0 remains contract-level"),
        ("Bmem_amplitude_promotion_allowed", False, "S3 helps rank one but cannot replace S_D; kappa/local gates remain open"),
    ]
    return [{"gate": gate, "status": pass_fail(ok), "evidence": evidence} for gate, ok, evidence in gates]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"key": "status", "value": STATUS},
        {"key": "claim_ceiling", "value": CLAIM_CEILING},
        {"key": "S3_rank_one_helpful", "value": "true_conditional"},
        {"key": "S3_replaces_SD", "value": "false"},
        {"key": "SD_parent_derived", "value": "false"},
        {"key": "Bmem_amplitude_derived", "value": "false"},
        {"key": "main_gain", "value": "S3_block_diagonalizes_cell_singlet_but_identifies_ordinary_singlet_leakage"},
        {"key": "main_blocker", "value": "parent_C_D_and_K_boundary_commutation_not_derived"},
        {"key": "next_action", "value": "either_derive_C_D_and_kernel_commutation_or_pivot_to_external_empirical_pressure_tests"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=None)
    args = parser.parse_args()

    timestamp = args.timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    script_path = Path(__file__).resolve()
    sources = source_register_rows(script_path)
    kernels = S3_kernel_rows()
    leakage = singlet_leakage_rows()
    sectors = sector_label_rows()
    clauses = theorem_clause_rows()
    gates = gate_rows(sources, kernels, leakage, sectors, clauses)
    decisions = decision_rows()

    write_csv(result_dir / "source_register.csv", sources, ["source", "role", "exists", "bytes"])
    write_csv(result_dir / "S3_kernel_decomposition.csv", kernels, ["kernel", "commutator_error", "singlet_doublet_cross_norm", "singlet_eigenvalue", "doublet_trace_average", "readout"])
    write_csv(result_dir / "singlet_leakage_tests.csv", leakage, ["source", "vector", "singlet_norm", "doublet_norm", "pure_singlet", "MTS_sector_by_S3_alone", "readout"])
    write_csv(result_dir / "SD_support_block_kernel.csv", sectors, ["kernel", "A_D_positive", "S_D_idempotence_error", "commutator_with_S_D", "ordinary_MTS_cross_norm", "readout"])
    write_csv(result_dir / "theorem_clauses.csv", clauses, ["clause", "needed_statement", "status", "evidence"])
    write_csv(result_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(result_dir / "decision.csv", decisions, ["key", "value"])

    payload = {
        "script": str(script_path),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "S3_rank_one_helpful": "true_conditional",
        "S3_replaces_SD": False,
        "SD_parent_derived": False,
        "Bmem_amplitude_derived": False,
        "main_blocker": "parent_C_D_and_K_boundary_commutation_not_derived",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(STATUS + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
