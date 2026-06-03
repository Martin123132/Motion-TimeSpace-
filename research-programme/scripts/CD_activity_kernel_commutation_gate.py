from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "CD-activity-kernel-commutation-gate"
STATUS = "CD_activity_and_kernel_commutation_conditional_parent_origin_not_derived"
CLAIM_CEILING = "conditional_CD_activity_gate_no_local_GR_or_Bmem_promotion"


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


def norm(matrix: np.ndarray) -> float:
    return float(np.linalg.norm(matrix))


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    sources = [
        (script_path, "this C_D activity/kernel commutation gate"),
        (ROOT / "273-Cperp-relative-exactness-C-sector.md", "scalar Cperp exactness failed"),
        (ROOT / "274-lifted-C-sector-form-holonomy-route.md", "lifted C-sector route"),
        (ROOT / "309-MTS-boundary-projector-contract-attempt.md", "P_MTS boundary projector contract"),
        (ROOT / "310-ordinary-MTS-sector-split-attempt.md", "ordinary/MTS sector split attempt"),
        (ROOT / "311-sector-label-SD-origin-attempt.md", "S_D support label predecessor"),
        (ROOT / "323-S3-sector-label-combined-gate.md", "S3 cannot replace S_D"),
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


def basis_rows() -> list[dict[str, Any]]:
    labels = basis_labels()
    properties = basis_properties()
    rows = []
    for index, label in enumerate(labels):
        prop = properties[index]
        rows.append({"index": index, "basis_state": label, **prop})
    return rows


def basis_labels() -> list[str]:
    return [
        "ordinary_coherent_IR_relative",
        "ordinary_coherent_IR_exact",
        "ordinary_coherent_UV_relative",
        "ordinary_noncoherent_IR_relative",
        "MTS_coherent_IR_relative",
        "MTS_coherent_UV_relative",
        "MTS_noncoherent_IR_relative",
        "edge_horizon_or_mixed_coherent_IR_relative",
    ]


def basis_properties() -> list[dict[str, Any]]:
    return [
        {"sector": "ordinary", "coherent": True, "IR": True, "relative_nonexact": True, "edge": False},
        {"sector": "ordinary", "coherent": True, "IR": True, "relative_nonexact": False, "edge": False},
        {"sector": "ordinary", "coherent": True, "IR": False, "relative_nonexact": True, "edge": False},
        {"sector": "ordinary", "coherent": False, "IR": True, "relative_nonexact": True, "edge": False},
        {"sector": "MTS", "coherent": True, "IR": True, "relative_nonexact": True, "edge": False},
        {"sector": "MTS", "coherent": True, "IR": False, "relative_nonexact": True, "edge": False},
        {"sector": "MTS", "coherent": False, "IR": True, "relative_nonexact": True, "edge": False},
        {"sector": "edge", "coherent": True, "IR": True, "relative_nonexact": True, "edge": True},
    ]


def projector_from_property(key: str, value: Any = True) -> np.ndarray:
    diagonal = [1.0 if prop[key] == value else 0.0 for prop in basis_properties()]
    return np.diag(diagonal)


def projectors() -> dict[str, np.ndarray]:
    identity = np.eye(len(basis_labels()))
    p_coh = projector_from_property("coherent", True)
    p_ir = projector_from_property("IR", True)
    p_rel = projector_from_property("relative_nonexact", True)
    p_mts = projector_from_property("sector", "MTS")
    p_ord = projector_from_property("sector", "ordinary")
    p_edge = projector_from_property("sector", "edge")
    c_base = p_rel @ p_ir @ p_coh
    c_mts = p_mts @ c_base
    return {
        "I": identity,
        "P_coh": p_coh,
        "P_IR": p_ir,
        "P_rel": p_rel,
        "P_MTS": p_mts,
        "P_ord": p_ord,
        "P_edge": p_edge,
        "C_base_Prel_PIR_Pcoh": c_base,
        "C_MTS_PMTS_Prel_PIR_Pcoh": c_mts,
    }


def selected_indices(matrix: np.ndarray) -> list[int]:
    diagonal = np.diag(matrix)
    return [index for index, value in enumerate(diagonal) if abs(float(value)) > 1.0e-12]


def projector_rows(matrices: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    rows = []
    for name in ["P_coh", "P_IR", "P_rel", "P_MTS", "C_base_Prel_PIR_Pcoh", "C_MTS_PMTS_Prel_PIR_Pcoh"]:
        matrix = matrices[name]
        chosen = selected_indices(matrix)
        rows.append(
            {
                "operator": name,
                "rank": int(np.linalg.matrix_rank(matrix, tol=1.0e-12)),
                "idempotence_error": norm(matrix @ matrix - matrix),
                "selected_indices": ";".join(str(index) for index in chosen),
                "selected_states": ";".join(basis_labels()[index] for index in chosen),
            }
        )
    return rows


def leakage_rows(matrices: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    rows = []
    c_base = matrices["C_base_Prel_PIR_Pcoh"]
    c_mts = matrices["C_MTS_PMTS_Prel_PIR_Pcoh"]
    for index, label in enumerate(basis_labels()):
        vector = np.zeros(len(basis_labels()))
        vector[index] = 1.0
        base_norm = float(np.linalg.norm(c_base @ vector))
        mts_norm = float(np.linalg.norm(c_mts @ vector))
        rows.append(
            {
                "basis_index": index,
                "basis_state": label,
                "sector": basis_properties()[index]["sector"],
                "C_base_norm": base_norm,
                "C_MTS_norm": mts_norm,
                "base_readout": "passes_C_base" if base_norm > 1.0e-12 else "killed_by_C_base",
                "MTS_readout": "passes_C_MTS" if mts_norm > 1.0e-12 else "killed_by_C_MTS",
                "ordinary_leakage_in_C_base": basis_properties()[index]["sector"] == "ordinary" and base_norm > 1.0e-12,
            }
        )
    return rows


def support_projector(matrix: np.ndarray) -> np.ndarray:
    diagonal = np.diag(matrix)
    return np.diag([1.0 if abs(float(value)) > 1.0e-12 else 0.0 for value in diagonal])


def activity_rows(matrices: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    rows = []
    for name in ["C_base_Prel_PIR_Pcoh", "C_MTS_PMTS_Prel_PIR_Pcoh"]:
        c_matrix = matrices[name]
        a_matrix = c_matrix.T @ c_matrix
        s_matrix = support_projector(a_matrix)
        eigenvalues = np.linalg.eigvalsh(a_matrix)
        rows.append(
            {
                "C_operator": name,
                "A_operator": f"A_{name}",
                "A_positive": bool(np.all(eigenvalues >= -1.0e-12)),
                "A_rank": int(np.linalg.matrix_rank(a_matrix, tol=1.0e-12)),
                "S_rank": int(np.linalg.matrix_rank(s_matrix, tol=1.0e-12)),
                "S_idempotence_error": norm(s_matrix @ s_matrix - s_matrix),
                "support_states": ";".join(basis_labels()[index] for index in selected_indices(s_matrix)),
            }
        )
    return rows


def kernel_rows(matrices: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    c_mts = matrices["C_MTS_PMTS_Prel_PIR_Pcoh"]
    a_mts = c_mts.T @ c_mts
    s_mts = support_projector(a_mts)
    p_ord = matrices["P_ord"]
    p_mts = matrices["P_MTS"]
    identity = matrices["I"]
    diagonal_kernel = np.diag([1.0, 1.2, 1.4, 1.6, 2.5, 2.7, 2.9, 3.1])
    activity_function_kernel = 2.0 * identity + 3.0 * a_mts
    mixing_kernel = diagonal_kernel.copy()
    mixing_kernel[0, 4] = 0.25
    mixing_kernel[4, 0] = 0.25
    edge_mixing_kernel = diagonal_kernel.copy()
    edge_mixing_kernel[4, 7] = 0.2
    edge_mixing_kernel[7, 4] = 0.2
    rows = []
    for name, kernel in [
        ("block_diagonal_by_sector", diagonal_kernel),
        ("function_of_A_D", activity_function_kernel),
        ("ordinary_MTS_mixing_counterexample", mixing_kernel),
        ("MTS_edge_mixing_counterexample", edge_mixing_kernel),
    ]:
        rows.append(
            {
                "kernel": name,
                "commutator_with_A_D": norm(kernel @ a_mts - a_mts @ kernel),
                "commutator_with_S_D": norm(kernel @ s_mts - s_mts @ kernel),
                "ordinary_MTS_cross_norm": norm(p_ord @ kernel @ p_mts) + norm(p_mts @ kernel @ p_ord),
                "MTS_edge_cross_norm": norm(p_mts @ kernel @ matrices["P_edge"]) + norm(matrices["P_edge"] @ kernel @ p_mts),
                "readout": "commutes_safe_if_parent_owned" if norm(kernel @ a_mts - a_mts @ kernel) < 1.0e-12 else "commutation_fails_cross_terms_allowed",
            }
        )
    return rows


def theorem_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "C1_base_activity_written",
            "needed_statement": "C_base=P_rel P_IR P_coh can be written as a coherent/IR/relative activity filter",
            "status": "pass_conditional",
            "evidence": "finite projector algebra selects coherent IR non-exact states",
        },
        {
            "clause": "C2_base_activity_not_enough",
            "needed_statement": "C_base alone must kill ordinary coherent baths",
            "status": "fail_no_go",
            "evidence": "ordinary_coherent_IR_relative passes C_base",
        },
        {
            "clause": "C3_MTS_channel_filter",
            "needed_statement": "an MTS-specific parent channel P_MTS or equivalent activity map kills ordinary coherent bath leakage",
            "status": "pass_conditional",
            "evidence": "C_MTS=P_MTS P_rel P_IR P_coh kills ordinary states in the toy basis",
        },
        {
            "clause": "C4_parent_PMTS_or_CD",
            "needed_statement": "parent action derives P_MTS or a channel-specific C_D rather than inserting it",
            "status": "not_derived",
            "evidence": "P_MTS/C_D remains the contract identified in checkpoints 309-323",
        },
        {
            "clause": "C5_activity_support",
            "needed_statement": "A_D=C_D^dagger C_D is positive and S_D=support(A_D) is a threshold-free projector",
            "status": "pass_conditional",
            "evidence": "matrix A_D is positive and S_D idempotent for supplied C_D",
        },
        {
            "clause": "C6_kernel_commutation",
            "needed_statement": "[K_boundary,A_D]=0 follows from parent boundary action",
            "status": "not_derived",
            "evidence": "commutation holds if K=f(A_D) or block diagonal, but generic kernels mix sectors",
        },
        {
            "clause": "C7_lifted_C_current",
            "needed_statement": "C_D is derived from a lifted 3-form/holonomy/domain current J_C",
            "status": "not_derived",
            "evidence": "checkpoint 274 identifies this as the future route, not a completed derivation",
        },
    ]


def gate_rows(
    sources: list[dict[str, Any]],
    projectors: list[dict[str, Any]],
    leakage: list[dict[str, Any]],
    activity: list[dict[str, Any]],
    kernels: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in sources)
    projector = {row["operator"]: row for row in projectors}
    activity_by_c = {row["C_operator"]: row for row in activity}
    kernel = {row["kernel"]: row for row in kernels}
    clause = {row["clause"]: row for row in clauses}
    ordinary_leaks = [row for row in leakage if row["ordinary_leakage_in_C_base"] is True]
    gates = [
        ("source_paths_exist", sources_ok, "all cited predecessor checkpoints and this script exist"),
        ("C_base_projector_written", float(projector["C_base_Prel_PIR_Pcoh"]["idempotence_error"]) < 1.0e-12, "P_rel P_IR P_coh is a valid projector in the toy boundary space"),
        ("C_base_ordinary_leakage_detected", len(ordinary_leaks) > 0, "ordinary coherent IR relative bath passes C_base"),
        ("C_MTS_kills_ordinary_leakage_if_supplied", all(float(row["C_MTS_norm"]) < 1.0e-12 for row in leakage if row["sector"] == "ordinary"), "C_MTS kills ordinary states if P_MTS is supplied"),
        ("A_D_positive_for_C_MTS", activity_by_c["C_MTS_PMTS_Prel_PIR_Pcoh"]["A_positive"] is True, "A_D=C_D^dagger C_D is positive"),
        ("S_D_support_idempotent", float(activity_by_c["C_MTS_PMTS_Prel_PIR_Pcoh"]["S_idempotence_error"]) < 1.0e-12, "support(A_D) is idempotent"),
        ("K_function_of_A_commutes", float(kernel["function_of_A_D"]["commutator_with_A_D"]) < 1.0e-12, "K=f(A_D) commutes with A_D"),
        ("generic_kernel_mixing_counterexample", kernel["ordinary_MTS_mixing_counterexample"]["readout"] == "commutation_fails_cross_terms_allowed", "generic boundary kernel can mix ordinary and MTS support"),
        ("edge_kernel_mixing_counterexample", kernel["MTS_edge_mixing_counterexample"]["readout"] == "commutation_fails_cross_terms_allowed", "edge/horizon channel can mix unless separately owned"),
        ("parent_C_D_derived", clause["C4_parent_PMTS_or_CD"]["status"] == "pass", "P_MTS/C_D remains underived"),
        ("parent_kernel_commutation_derived", clause["C6_kernel_commutation"]["status"] == "pass", "[K_boundary,A_D]=0 remains underived"),
        ("lifted_JC_parent_derived", clause["C7_lifted_C_current"]["status"] == "pass", "lifted J_C route remains future theorem target"),
        ("local_GR_or_Bmem_promotion_allowed", False, "C_D and kernel commutation are conditional, not parent-derived"),
    ]
    return [{"gate": gate, "status": pass_fail(ok), "evidence": evidence} for gate, ok, evidence in gates]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"key": "status", "value": STATUS},
        {"key": "claim_ceiling", "value": CLAIM_CEILING},
        {"key": "C_base_sufficient", "value": "false"},
        {"key": "C_MTS_sufficient_if_supplied", "value": "conditional"},
        {"key": "parent_C_D_derived", "value": "false"},
        {"key": "parent_kernel_commutation_derived", "value": "false"},
        {"key": "local_GR_derived", "value": "false"},
        {"key": "Bmem_amplitude_derived", "value": "false"},
        {"key": "main_gain", "value": "exact_leakage_and_commutation_gates_written"},
        {"key": "main_blocker", "value": "parent_P_MTS_or_C_D_and_K_boundary_commutation_not_derived"},
        {"key": "next_action", "value": "park_projector_branch_as_conditional_and_move_to_external_empirical_pressure_unless_new_parent_action_supplies_C_D"},
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
    matrices = projectors()
    basis = basis_rows()
    projectors_table = projector_rows(matrices)
    leakage = leakage_rows(matrices)
    activity = activity_rows(matrices)
    kernels = kernel_rows(matrices)
    clauses = theorem_clause_rows()
    gates = gate_rows(sources, projectors_table, leakage, activity, kernels, clauses)
    decisions = decision_rows()

    write_csv(result_dir / "source_register.csv", sources, ["source", "role", "exists", "bytes"])
    write_csv(result_dir / "boundary_basis.csv", basis, ["index", "basis_state", "sector", "coherent", "IR", "relative_nonexact", "edge"])
    write_csv(result_dir / "CD_projector_algebra.csv", projectors_table, ["operator", "rank", "idempotence_error", "selected_indices", "selected_states"])
    write_csv(result_dir / "ordinary_leakage_tests.csv", leakage, ["basis_index", "basis_state", "sector", "C_base_norm", "C_MTS_norm", "base_readout", "MTS_readout", "ordinary_leakage_in_C_base"])
    write_csv(result_dir / "activity_support.csv", activity, ["C_operator", "A_operator", "A_positive", "A_rank", "S_rank", "S_idempotence_error", "support_states"])
    write_csv(result_dir / "kernel_commutation.csv", kernels, ["kernel", "commutator_with_A_D", "commutator_with_S_D", "ordinary_MTS_cross_norm", "MTS_edge_cross_norm", "readout"])
    write_csv(result_dir / "theorem_clauses.csv", clauses, ["clause", "needed_statement", "status", "evidence"])
    write_csv(result_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(result_dir / "decision.csv", decisions, ["key", "value"])

    payload = {
        "script": str(script_path),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "C_base_sufficient": False,
        "C_MTS_sufficient_if_supplied": "conditional",
        "parent_C_D_derived": False,
        "parent_kernel_commutation_derived": False,
        "local_GR_derived": False,
        "Bmem_amplitude_derived": False,
        "main_blocker": "parent_P_MTS_or_C_D_and_K_boundary_commutation_not_derived",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(STATUS + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
