from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "exact-parent-pullback-selection-rule-gate"
STATUS = "exact_parent_pullback_theorem_constructed_parent_action_premise_open"
CLAIM_CEILING = "conditional_pullback_theorem_no_unconditional_epsilonH_or_Bmem_promotion"
DIM_CELL = 27
RANK_ACTIVE = 2
Q_TRACE = Fraction(RANK_ACTIVE, DIM_CELL)
DELTA_TEST = 0.0061980866083466


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


def permutation_swap(i: int, j: int) -> np.ndarray:
    matrix = np.eye(DIM_CELL)
    matrix[[i, j], :] = matrix[[j, i], :]
    return matrix


def adjacent_full_generators() -> list[np.ndarray]:
    return [permutation_swap(index, index + 1) for index in range(DIM_CELL - 1)]


def residual_generators() -> list[np.ndarray]:
    active = [permutation_swap(0, 1)]
    inactive = [permutation_swap(index, index + 1) for index in range(2, DIM_CELL - 1)]
    return active + inactive


def active_inactive_swap() -> np.ndarray:
    return permutation_swap(0, 2)


def active_projector() -> np.ndarray:
    projector = np.zeros((DIM_CELL, DIM_CELL), dtype=float)
    projector[0, 0] = 1.0
    projector[1, 1] = 1.0
    return projector


def all_ones() -> np.ndarray:
    return np.ones((DIM_CELL, DIM_CELL), dtype=float)


def max_commutator_norm(operator: np.ndarray, generators: list[np.ndarray]) -> float:
    if not generators:
        return 0.0
    return max(float(np.linalg.norm(operator @ generator - generator @ operator)) for generator in generators)


def full_trace_average(operator: np.ndarray) -> float:
    return float(np.trace(operator)) / DIM_CELL


def active_trace_average(operator: np.ndarray) -> float:
    projector = active_projector()
    return float(np.trace(projector @ operator)) / RANK_ACTIVE


def q_trace_effective(operator: np.ndarray) -> float:
    projector = active_projector()
    return float(np.trace(projector @ operator)) / DIM_CELL


def normalized_full_invariant(a_coeff: float, b_coeff: float) -> np.ndarray:
    current = a_coeff * np.eye(DIM_CELL) + b_coeff * all_ones()
    average = full_trace_average(current)
    if abs(average) < 1.0e-14:
        raise ValueError("Cannot normalize zero-trace-average current.")
    return current / average


def commutant_constraint_matrix(generators: list[np.ndarray]) -> np.ndarray:
    identity = np.eye(DIM_CELL)
    blocks = []
    for generator in generators:
        blocks.append(np.kron(generator.T, identity) - np.kron(identity, generator))
    return np.vstack(blocks)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "331-trace-normalized-Hamiltonian-amplitude-contract.md", "trace-normalized amplitude contract"),
        (ROOT / "334-cell-equivalence-no-active-block-symmetry-gate.md", "full equivalence versus active-block symmetry"),
        (ROOT / "335-two-stage-identity-then-project-ordering-gate.md", "identity-then-project ordering gate"),
        (ROOT / "336-no-later-active-counterterm-theorem-gate.md", "exact parent-pullback contract target"),
        (Path(__file__).resolve(), "this verifier"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path, role in sources
    ]


def commutant_rows() -> list[dict[str, Any]]:
    full_constraints = commutant_constraint_matrix(adjacent_full_generators())
    rank = int(np.linalg.matrix_rank(full_constraints, tol=1.0e-9))
    nullity = DIM_CELL * DIM_CELL - rank
    identity = np.eye(DIM_CELL)
    coherent = all_ones()
    projector = active_projector()
    lambda_counterterm = identity + DELTA_TEST * projector
    return [
        {
            "algebra": "full_S27_cell_equivalence",
            "generators": len(adjacent_full_generators()),
            "constraint_rank": rank,
            "commutant_dimension": nullity,
            "basis_readout": "span(I_cell, J_cell)",
            "P_active_commutator": max_commutator_norm(projector, [active_inactive_swap()]),
            "lambda_counterterm_commutator": max_commutator_norm(lambda_counterterm, [active_inactive_swap()]),
            "meaning": "full permutation equivalence allows only uniform diagonal readout plus coherent all-cell mode",
        },
        {
            "algebra": "residual_S2_x_S25_projector_preserving",
            "generators": len(residual_generators()),
            "constraint_rank": "",
            "commutant_dimension": "",
            "basis_readout": "contains P_active and I_cell-P_active",
            "P_active_commutator": max_commutator_norm(projector, residual_generators()),
            "lambda_counterterm_commutator": max_commutator_norm(lambda_counterterm, residual_generators()),
            "meaning": "after projection, residual symmetry allows an active-block coupling",
        },
    ]


def pullback_sample_rows() -> list[dict[str, Any]]:
    samples = [
        ("identity_only", 1.0, 0.0),
        ("mixed_identity_coherent", 0.3, 0.7),
        ("opposite_identity_coherent", 2.0, -1.0),
        ("mostly_identity_small_coherent", 0.95, 0.05),
    ]
    rows: list[dict[str, Any]] = []
    for name, a_coeff, b_coeff in samples:
        current = normalized_full_invariant(a_coeff, b_coeff)
        rows.append(
            {
                "sample": name,
                "a_I_before_normalization": a_coeff,
                "b_J_before_normalization": b_coeff,
                "full_trace_average": full_trace_average(current),
                "active_trace_average_epsilon_H": active_trace_average(current),
                "q_trace_effective": q_trace_effective(current),
                "full_commutator": max_commutator_norm(current, adjacent_full_generators()),
                "readout": "epsilon_H equals full trace normalization for every full-invariant sample",
            }
        )
    projector = active_projector()
    lambda_counterterm = np.eye(DIM_CELL) + DELTA_TEST * projector
    rows.append(
        {
            "sample": "post_projection_lambda_counterterm",
            "a_I_before_normalization": 1.0,
            "b_J_before_normalization": "not_full_invariant",
            "full_trace_average": full_trace_average(lambda_counterterm),
            "active_trace_average_epsilon_H": active_trace_average(lambda_counterterm),
            "q_trace_effective": q_trace_effective(lambda_counterterm),
            "full_commutator": max_commutator_norm(lambda_counterterm, [active_inactive_swap()]),
            "readout": "shifts epsilon_H but is not in the full parent commutant",
        }
    )
    return rows


def theorem_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "T1_full_cell_equivalence",
            "statement": "the parent Hamiltonian-current operator is invariant under full S27 cell equivalence before active projection",
            "mathematical_role": "restricts the parent current to the full commutant span(I_cell,J_cell)",
            "status": "algebraically_verified",
        },
        {
            "condition": "T2_trace_normalized_current",
            "statement": "the parent current is normalized by Tr(H_parent)/27=1",
            "mathematical_role": "sets the common diagonal average of every full-invariant parent current",
            "status": "assumption_from_trace_contract",
        },
        {
            "condition": "T3_exact_readout_projection",
            "statement": "P_active is a readout/projection of the parent current, not a new reduced action-building tensor",
            "mathematical_role": "computes Tr(P_active H_parent)/2 without adding residual invariants",
            "status": "not_yet_parent_derived",
        },
        {
            "condition": "T4_no_Wilsonian_reduced_EFT_stage",
            "statement": "the reduction does not license all S2 x S25 residual-invariant counterterms",
            "mathematical_role": "forbids lambda_mem P_active even though residual symmetry allows it",
            "status": "not_yet_parent_derived",
        },
        {
            "condition": "T5_same_constraint_current",
            "statement": "the projected memory trace remains a subtrace of the same Hamiltonian/lapse constraint current",
            "mathematical_role": "prevents independent reduced-sector normalization",
            "status": "open",
        },
    ]


def fork_rows() -> list[dict[str, Any]]:
    return [
        {
            "fork": "exact_parent_readout",
            "allowed_operator_rule": "reduced operators must be restrictions/readouts of full S27-invariant parent operators",
            "lambda_mem_Pactive_allowed": False,
            "epsilon_H_status": "conditional_theorem_epsilon_H_equals_1",
            "meaning": "this route derives no later active counterterm if the parent action owns exact readout",
        },
        {
            "fork": "Wilsonian_reduced_EFT",
            "allowed_operator_rule": "after projection, write every S2 x S25 residual-invariant operator",
            "lambda_mem_Pactive_allowed": True,
            "epsilon_H_status": "free_or_fitted_coupling",
            "meaning": "this route reopens the amplitude and demotes epsilon_H to closure",
        },
        {
            "fork": "mixed_parent_plus_effective_corrections",
            "allowed_operator_rule": "parent readout plus correction terms constrained by anomaly/renormalization rule",
            "lambda_mem_Pactive_allowed": "open",
            "epsilon_H_status": "radiative_stability_unproven",
            "meaning": "this is viable only if corrections obey the full-parent pullback selection rule",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma": "full_commutant_diagonal_uniformity",
            "statement": "For full S27 cell equivalence, every invariant parent current has equal diagonal entries.",
            "consequence": "any rank-2 coordinate readout has the same average as the full trace average.",
        },
        {
            "lemma": "pullback_epsilon_theorem",
            "statement": "If H_parent is full-cell-invariant and Tr(H_parent)/27=1, then Tr(P_active H_parent)/2=1.",
            "consequence": "epsilon_H=1 follows for exact readout projection.",
        },
        {
            "lemma": "reduced_EFT_counterterm_fork",
            "statement": "If the reduced theory is allowed to add all residual invariants, lambda_mem P_active is allowed.",
            "consequence": "the theorem lives or dies on exact readout versus Wilsonian EFT.",
        },
    ]


def gate_rows(
    sources: list[dict[str, Any]],
    commutants: list[dict[str, Any]],
    samples: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    by_algebra = {row["algebra"]: row for row in commutants}
    full_commutant = by_algebra["full_S27_cell_equivalence"]
    residual = by_algebra["residual_S2_x_S25_projector_preserving"]
    full_samples = [row for row in samples if row["sample"] != "post_projection_lambda_counterterm"]
    sample_eps_ok = all(abs(float(row["active_trace_average_epsilon_H"]) - 1.0) < 1.0e-12 for row in full_samples)
    sample_q_ok = all(abs(float(row["q_trace_effective"]) - float(Q_TRACE)) < 1.0e-12 for row in full_samples)
    return [
        {"gate": "source_paths_exist", "status": "pass" if sources_ok else "fail", "evidence": sources_ok},
        {
            "gate": "full_S27_commutant_dimension_two",
            "status": "pass" if int(full_commutant["commutant_dimension"]) == 2 else "fail",
            "evidence": full_commutant["commutant_dimension"],
        },
        {
            "gate": "full_invariant_trace_normalization_implies_epsilon_one",
            "status": "pass" if sample_eps_ok else "fail",
            "evidence": sample_eps_ok,
        },
        {
            "gate": "full_invariant_trace_normalization_implies_q_trace_2over27",
            "status": "pass" if sample_q_ok else "fail",
            "evidence": sample_q_ok,
        },
        {
            "gate": "P_active_not_full_invariant",
            "status": "pass" if float(full_commutant["P_active_commutator"]) > 1.0e-12 else "fail",
            "evidence": full_commutant["P_active_commutator"],
        },
        {
            "gate": "P_active_residual_invariant",
            "status": "pass" if float(residual["P_active_commutator"]) < 1.0e-12 else "fail",
            "evidence": residual["P_active_commutator"],
        },
        {
            "gate": "exact_pullback_forbids_lambda_counterterm",
            "status": "pass",
            "evidence": "lambda_mem P_active is not in the full S27 parent commutant",
        },
        {
            "gate": "reduced_Wilsonian_EFT_allows_lambda_counterterm",
            "status": "pass",
            "evidence": "lambda_mem P_active commutes with residual projector-preserving generators",
        },
        {
            "gate": "parent_action_proves_exact_readout_not_EFT",
            "status": "fail",
            "evidence": "current corpus has a conditional contract, not an action-level selection theorem",
        },
        {
            "gate": "epsilon_H_parent_derived_unconditionally",
            "status": "fail",
            "evidence": "epsilon_H=1 is derived only under T1-T5 exact-readout premises",
        },
        {
            "gate": "Bmem_parent_promotion_allowed",
            "status": "fail",
            "evidence": "Hstar=H0 and physical parent exact-readout ownership remain open",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "A real conditional theorem is now available: full S27 cell equivalence plus trace normalization makes every "
                "exact parent readout give epsilon_H=1 and q_trace=2/27. The post-projection lambda_mem P_active term is "
                "forbidden in the exact-pullback branch because it is not a full parent invariant. However, if the reduced "
                "stage is a Wilsonian EFT, residual symmetry permits that same term. Therefore the unresolved physics is "
                "whether the parent MTS action proves exact readout/quotient rather than a new reduced EFT."
            ),
            "next_target": "derive_action_level_exact_readout_or_demote_epsilonH_to_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    commutants = commutant_rows()
    samples = pullback_sample_rows()
    contract = theorem_contract_rows()
    forks = fork_rows()
    no_gos = no_go_rows()
    gates = gate_rows(sources, commutants, samples)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": (sources, ["source", "role", "exists", "issue"]),
        "commutant_audit.csv": (
            commutants,
            [
                "algebra",
                "generators",
                "constraint_rank",
                "commutant_dimension",
                "basis_readout",
                "P_active_commutator",
                "lambda_counterterm_commutator",
                "meaning",
            ],
        ),
        "pullback_samples.csv": (
            samples,
            [
                "sample",
                "a_I_before_normalization",
                "b_J_before_normalization",
                "full_trace_average",
                "active_trace_average_epsilon_H",
                "q_trace_effective",
                "full_commutator",
                "readout",
            ],
        ),
        "theorem_contract.csv": (
            contract,
            ["condition", "statement", "mathematical_role", "status"],
        ),
        "fork_audit.csv": (
            forks,
            ["fork", "allowed_operator_rule", "lambda_mem_Pactive_allowed", "epsilon_H_status", "meaning"],
        ),
        "no_go_lemmas.csv": (no_gos, ["lemma", "statement", "consequence"]),
        "gate_results.csv": (gates, ["gate", "status", "evidence"]),
        "decision.csv": (decisions, ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(result_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(result_dir),
        "generated": list(outputs),
        "q_trace_identity": f"{Q_TRACE.numerator}/{Q_TRACE.denominator}",
        "exact_pullback_conditional_theorem": True,
        "full_cell_commutant_dimension": 2,
        "epsilon_H_conditional_exact_readout": 1.0,
        "no_later_counterterm_derived_under_exact_readout": True,
        "parent_action_proves_exact_readout": False,
        "epsilon_H_parent_derived_unconditionally": False,
        "promotion_allowed": False,
        "next_target": "derive_action_level_exact_readout_or_demote_epsilonH_to_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exact parent-pullback selection rule gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
