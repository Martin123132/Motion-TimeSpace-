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
RUN_SLUG = "literal-projected-Hamiltonian-subblock-gate"
STATUS = "literal_Hamiltonian_subblock_template_constructed_parent_symmetry_missing_epsilonH_not_derived"
CLAIM_CEILING = "conditional_projected_Hamiltonian_template_no_Bmem_or_local_GR_promotion"
DIM_CELL = 27
RANK_ACTIVE = 2
Q_TRACE = Fraction(RANK_ACTIVE, DIM_CELL)


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


def active_projector() -> np.ndarray:
    projector = np.zeros((DIM_CELL, DIM_CELL), dtype=float)
    projector[0, 0] = 1.0
    projector[1, 1] = 1.0
    return projector


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "252-topological-projector-parent-action-skeleton.md", "topological projector parent skeleton"),
        (ROOT / "253-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure.md", "FLRW reduction and rank target"),
        (ROOT / "254-rank-27-rank-2-cell-theorem-or-Bmem-closure-lock.md", "rank-27/rank-2 theorem attempt"),
        (ROOT / "259-memory-stress-normalization-theorem-attempt.md", "kappa=1 theorem contract"),
        (ROOT / "260-C3-unit-stress-normalization-parent-action-attempt.md", "stress form and scale-lock split"),
        (ROOT / "326-radial-memory-parent-action-contract.md", "active projector trace and survival kernel"),
        (ROOT / "331-trace-normalized-Hamiltonian-amplitude-contract.md", "trace-normalized amplitude factorization"),
        (ROOT / "332-parent-Hamiltonian-trace-current-gate.md", "parent Hamiltonian trace-current gate"),
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


def matrix_summary(label: str, hamiltonian: np.ndarray, interpretation: str, status: str) -> dict[str, Any]:
    projector = active_projector()
    active_trace = float(np.trace(projector @ hamiltonian))
    normalized_active_trace = active_trace / DIM_CELL
    epsilon_inferred = normalized_active_trace / float(Q_TRACE)
    commutator_norm = float(np.linalg.norm(projector @ hamiltonian - hamiltonian @ projector))
    idempotence_error = float(np.linalg.norm(projector @ projector - projector))
    return {
        "case": label,
        "dim_cell": DIM_CELL,
        "rank_active": RANK_ACTIVE,
        "q_trace": float(Q_TRACE),
        "active_trace": active_trace,
        "normalized_active_trace": normalized_active_trace,
        "epsilon_H_inferred": epsilon_inferred,
        "commutator_norm": commutator_norm,
        "projector_idempotence_error": idempotence_error,
        "status": status,
        "interpretation": interpretation,
    }


def subblock_algebra_rows() -> list[dict[str, Any]]:
    identity = np.eye(DIM_CELL)
    projector = active_projector()
    lambda_mem = 1.0061980866083466
    diagonal_weight = np.eye(DIM_CELL)
    diagonal_weight[0, 0] = 0.991149235153442
    diagonal_weight[1, 1] = 1.0212469380632512
    noncommuting = np.eye(DIM_CELL)
    noncommuting[0, 2] = 0.25
    noncommuting[2, 0] = 0.25
    return [
        matrix_summary(
            "identity_coupled_parent_current",
            identity,
            "If the parent Hamiltonian current is identity-coupled over the cell space, active projection gives q_trace with epsilon_H=1.",
            "conditional_template_pass",
        ),
        matrix_summary(
            "lambda_active_rescaled_commuting_block",
            identity + (lambda_mem - 1.0) * projector,
            "A commuting active-block rescaling preserves projector algebra but changes the amplitude; parent symmetry must forbid it.",
            "counterexample_lambda_free",
        ),
        matrix_summary(
            "active_only_inserted_parent_block",
            projector,
            "Putting only the active block in the parent gives the desired fraction by construction, but it is just the projector inserted upstream.",
            "imposition_not_derivation",
        ),
        matrix_summary(
            "weighted_cell_parent_current",
            diagonal_weight,
            "Unequal active cell weights commute with P_active but shift epsilon_H unless cell-equivalence symmetry fixes the trace measure.",
            "counterexample_cell_weight_free",
        ),
        matrix_summary(
            "noncommuting_mixed_parent_current",
            noncommuting,
            "A parent current that mixes active and inactive sectors keeps a similar trace but fails the support-commutation/local-silence gate.",
            "counterexample_noncommuting",
        ),
    ]


def theorem_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "S1_parent_cell_space",
            "required_statement": "V_cell is parent-owned with dim(V_cell)=27.",
            "current_status": "conditional_not_parent_derived",
            "why_needed": "without the cell space, the denominator is bookkeeping",
        },
        {
            "condition": "S2_parent_active_projector",
            "required_statement": "P_active is parent-owned, idempotent, trace two, and sector/support selected before scoring.",
            "current_status": "conditional_not_parent_derived",
            "why_needed": "without this, the numerator is chosen to hit the target",
        },
        {
            "condition": "S3_identity_cell_coupling",
            "required_statement": "the parent Hamiltonian current is proportional to the identity on V_cell before active projection.",
            "current_status": "missing_core_symmetry",
            "why_needed": "this is what forces epsilon_H=1 rather than an active-block weight",
        },
        {
            "condition": "S4_no_active_block_invariant",
            "required_statement": "a symmetry/quotient principle forbids lambda_mem P_active H_parent as a separate invariant.",
            "current_status": "not_derived",
            "why_needed": "lambda_active_rescaled_commuting_block is otherwise allowed",
        },
        {
            "condition": "S5_support_commutation",
            "required_statement": "[P_active,H_parent]=0 or the noncommuting pieces are pure gauge/constraint-null.",
            "current_status": "conditional_not_parent_derived",
            "why_needed": "noncommuting current leaks active/inactive sectors and threatens local silence",
        },
        {
            "condition": "S6_same_lapse_Hamiltonian",
            "required_statement": "the projected subblock is varied by the same lapse as the background Hamiltonian constraint.",
            "current_status": "not_derived",
            "why_needed": "otherwise the memory term is an independent Hamiltonian sector",
        },
        {
            "condition": "S7_activation_without_amplitude",
            "required_statement": "F(N) gates the inherited current but carries no independent coefficient.",
            "current_status": "conditional_survival_kernel_only",
            "why_needed": "otherwise the missing amplitude moves into the activation sector",
        },
        {
            "condition": "S8_scale_lock",
            "required_statement": "H_star=H0 or equivalent scale-lock is parent-derived.",
            "current_status": "closure_locked",
            "why_needed": "epsilon_H=1 is not enough if the stress scale remains free",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "no_go": "commuting_lambda_block",
            "counterexample": "H_parent = I + (lambda_mem-1)P_active",
            "result": "commutes with P_active but gives epsilon_H=lambda_mem on the active trace",
            "consequence": "commutation and Bianchi safety do not prove unit inheritance",
        },
        {
            "no_go": "weighted_cell_trace",
            "counterexample": "active cells have unequal Hamiltonian weights",
            "result": "the projected trace shifts even with no active/inactive mixing",
            "consequence": "cell-equivalence or canonical trace measure must be parent-derived",
        },
        {
            "no_go": "active_block_inserted_upstream",
            "counterexample": "H_parent=P_active H_scale",
            "result": "desired trace appears only because the target projector was inserted into the parent current",
            "consequence": "this is closure unless a parent symmetry forces it",
        },
        {
            "no_go": "noncommuting_parent_current",
            "counterexample": "H_parent has active/inactive mixing terms",
            "result": "the trace may look harmless while the commutator exposes sector leakage",
            "consequence": "support commutation is a separate theorem gate",
        },
    ]


def gate_rows(sources: list[dict[str, Any]], algebra: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    by_case = {row["case"]: row for row in algebra}
    identity_ok = abs(float(by_case["identity_coupled_parent_current"]["epsilon_H_inferred"]) - 1.0) < 1.0e-12
    lambda_shifts = abs(float(by_case["lambda_active_rescaled_commuting_block"]["epsilon_H_inferred"]) - 1.0) > 1.0e-6
    weighted_shifts = abs(float(by_case["weighted_cell_parent_current"]["epsilon_H_inferred"]) - 1.0) > 1.0e-4
    noncommutes = float(by_case["noncommuting_mixed_parent_current"]["commutator_norm"]) > 1.0e-12
    return [
        {"gate": "source_paths_exist", "status": "pass" if sources_ok else "fail", "evidence": sources_ok},
        {"gate": "identity_subblock_gives_unit_epsilon", "status": "pass" if identity_ok else "fail", "evidence": by_case["identity_coupled_parent_current"]["epsilon_H_inferred"]},
        {"gate": "lambda_commuting_counterexample", "status": "pass" if lambda_shifts else "fail", "evidence": by_case["lambda_active_rescaled_commuting_block"]["epsilon_H_inferred"]},
        {"gate": "weighted_cell_counterexample", "status": "pass" if weighted_shifts else "fail", "evidence": by_case["weighted_cell_parent_current"]["epsilon_H_inferred"]},
        {"gate": "noncommuting_leak_counterexample", "status": "pass" if noncommutes else "fail", "evidence": by_case["noncommuting_mixed_parent_current"]["commutator_norm"]},
        {"gate": "cell_identity_coupling_parent_derived", "status": "fail", "evidence": "missing symmetry/constraint deriving H_parent proportional to I_cell"},
        {"gate": "no_active_block_invariant_parent_derived", "status": "fail", "evidence": "lambda_mem P_active H_parent not yet forbidden by parent principle"},
        {"gate": "literal_projected_subblock_parent_derived", "status": "fail", "evidence": "template constructed; parent derivation not supplied"},
        {"gate": "epsilon_H_parent_derived", "status": "fail", "evidence": "conditional template only"},
        {"gate": "Bmem_parent_promotion_allowed", "status": "fail", "evidence": "rank trace, scale-lock, and subblock inheritance remain conditional/open"},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The literal subblock construction works algebraically only in the identity-coupled parent-current case. "
                "That gives epsilon_H=1 as a conditional theorem template. But commuting lambda and weighted-cell "
                "counterexamples show that the parent action must still derive cell-equivalence/identity coupling and "
                "forbid independent active-block invariants. Without that symmetry, epsilon_H remains closure/fitted."
            ),
            "best_next_target": "derive_cell_equivalence_or_no_active_block_invariant_symmetry",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    algebra = subblock_algebra_rows()
    conditions = theorem_condition_rows()
    no_go = no_go_rows()
    gates = gate_rows(sources, algebra)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": (sources, ["source", "role", "exists", "issue"]),
        "subblock_algebra.csv": (
            algebra,
            [
                "case",
                "dim_cell",
                "rank_active",
                "q_trace",
                "active_trace",
                "normalized_active_trace",
                "epsilon_H_inferred",
                "commutator_norm",
                "projector_idempotence_error",
                "status",
                "interpretation",
            ],
        ),
        "theorem_conditions.csv": (conditions, ["condition", "required_statement", "current_status", "why_needed"]),
        "no_go_lemmas.csv": (no_go, ["no_go", "counterexample", "result", "consequence"]),
        "gate_results.csv": (gates, ["gate", "status", "evidence"]),
        "decision.csv": (decisions, ["decision", "claim_ceiling", "meaning", "best_next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(result_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(result_dir),
        "generated": list(outputs),
        "q_trace": f"{Q_TRACE.numerator}/{Q_TRACE.denominator}",
        "literal_subblock_template_constructed": True,
        "epsilon_H_parent_derived": False,
        "promotion_allowed": False,
        "next_target": "derive_cell_equivalence_or_no_active_block_invariant_symmetry",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Construct or reject literal projected-Hamiltonian subblock route.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
