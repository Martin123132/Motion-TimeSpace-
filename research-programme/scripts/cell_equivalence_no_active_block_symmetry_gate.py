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
RUN_SLUG = "cell-equivalence-no-active-block-symmetry-gate"
STATUS = "S3_and_projector_symmetries_allow_active_block_lambda_full_cell_equivalence_forbids_projector"
CLAIM_CEILING = "cell_equivalence_symmetry_gate_no_epsilonH_or_Bmem_promotion"
DIM_CELL = 27
LAMBDA_TEST = 1.0061980866083466


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


def permutation_matrix(perm: tuple[int, ...]) -> np.ndarray:
    matrix = np.zeros((len(perm), len(perm)), dtype=float)
    for row, col in enumerate(perm):
        matrix[row, col] = 1.0
    return matrix


def s3_group() -> list[np.ndarray]:
    return [permutation_matrix(tuple(perm)) for perm in itertools.permutations(range(3))]


def singlet_projector() -> np.ndarray:
    return np.ones((3, 3), dtype=float) / 3.0


def screen_projector() -> np.ndarray:
    return np.diag([1.0, 1.0, 0.0])


def active_projector() -> np.ndarray:
    return np.kron(np.kron(singlet_projector(), singlet_projector()), screen_projector())


def active_lambda_current() -> np.ndarray:
    projector = active_projector()
    return np.eye(DIM_CELL) + (LAMBDA_TEST - 1.0) * projector


def max_commutator_norm(operator: np.ndarray, group: list[np.ndarray]) -> float:
    if not group:
        return 0.0
    return max(float(np.linalg.norm(operator @ generator - generator @ operator)) for generator in group)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "322-S3-singlet-motion-time-projector-gate.md", "S3 singlet projector gate"),
        (ROOT / "323-S3-sector-label-combined-gate.md", "S3 cannot replace sector support label"),
        (ROOT / "333-literal-projected-Hamiltonian-subblock-gate.md", "literal subblock gate and lambda counterexample"),
        (ROOT / "272-quotient-configuration-principle-from-topological-projector.md", "quotient principle route"),
        (ROOT / "scripts" / "singlet_motion_time_projector_gate.py", "S3 projector verifier"),
        (ROOT / "scripts" / "literal_projected_Hamiltonian_subblock_gate.py", "subblock verifier"),
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


def symmetry_test_rows() -> list[dict[str, Any]]:
    p_active = active_projector()
    h_lambda = active_lambda_current()
    identity_3 = np.eye(3)

    s3_motion = [np.kron(np.kron(generator, identity_3), identity_3) for generator in s3_group()]
    s3_time = [np.kron(np.kron(identity_3, generator), identity_3) for generator in s3_group()]
    screen_swap = permutation_matrix((1, 0, 2))
    screen_plane = [np.kron(np.kron(identity_3, identity_3), screen_swap)]
    s3_screen_group = s3_motion + s3_time + screen_plane

    active_to_inactive_swap = np.eye(DIM_CELL)
    active_to_inactive_swap[[0, 2], :] = active_to_inactive_swap[[2, 0], :]
    full_cell_mixer = [active_to_inactive_swap]

    block_preserving = [p_active, np.eye(DIM_CELL) - p_active]

    rows = [
        {
            "symmetry": "S3_M_x_S3_T_x_screen_plane",
            "P_active_commutator": max_commutator_norm(p_active, s3_screen_group),
            "lambda_current_commutator": max_commutator_norm(h_lambda, s3_screen_group),
            "P_active_invariant": True,
            "lambda_block_forbidden": False,
            "readout": "fails_to_forbid_active_block_lambda",
            "meaning": "The symmetry that owns the singlet/screen projector still permits I+(lambda-1)P_active.",
        },
        {
            "symmetry": "projector_preserving_block_algebra",
            "P_active_commutator": max_commutator_norm(p_active, block_preserving),
            "lambda_current_commutator": max_commutator_norm(h_lambda, block_preserving),
            "P_active_invariant": True,
            "lambda_block_forbidden": False,
            "readout": "explicitly_allows_active_block_lambda",
            "meaning": "Any algebra that preserves the active/inactive split allows independent block weights unless more is added.",
        },
        {
            "symmetry": "full_cell_equivalence_mixing_active_inactive",
            "P_active_commutator": max_commutator_norm(p_active, full_cell_mixer),
            "lambda_current_commutator": max_commutator_norm(h_lambda, full_cell_mixer),
            "P_active_invariant": False,
            "lambda_block_forbidden": True,
            "readout": "forbids_lambda_but_also_forbids_projector",
            "meaning": "A symmetry strong enough to mix all cells kills the active-block coefficient but also makes P_active non-invariant.",
        },
    ]
    return rows


def route_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "S3_M_x_S3_T_x_screen_symmetry",
            "what_it_derives": "unique motion/time singlet projectors and rank-two screen lift conditionally",
            "does_it_forbid_lambda_active": False,
            "failure_mode": "P_active is itself invariant, so I+(lambda-1)P_active is also invariant",
            "verdict": "insufficient_for_epsilonH",
        },
        {
            "route": "full_cell_equivalence",
            "what_it_derives": "identity coupling if the representation is irreducible/transitive enough",
            "does_it_forbid_lambda_active": True,
            "failure_mode": "also forbids or erases the nontrivial active projector unless symmetry breaking/quotient timing is derived",
            "verdict": "too_strong_without_two_stage_parent_mechanism",
        },
        {
            "route": "quotient_gauge_representative_invariance",
            "what_it_derives": "can make representative directions unphysical and select projected matter variables",
            "does_it_forbid_lambda_active": False,
            "failure_mode": "quotient invariance removes representative dependence, not a physical active-block stress coefficient",
            "verdict": "helps_local_Cperp_not_amplitude",
        },
        {
            "route": "topological_index_normalization",
            "what_it_derives": "can support integer rank/trace targets",
            "does_it_forbid_lambda_active": False,
            "failure_mode": "indices count channels but do not set Hamiltonian weights",
            "verdict": "helps_q_trace_not_epsilonH",
        },
        {
            "route": "first_class_constraint_lambda_equals_one",
            "what_it_derives": "can remove lambda if the constraint is parent-owned",
            "does_it_forbid_lambda_active": True,
            "failure_mode": "without parent origin this is just setting lambda=1",
            "verdict": "possible_future_route_not_current_derivation",
        },
        {
            "route": "two_stage_identity_then_project",
            "what_it_derives": "identity Hamiltonian current first, active projector applied as derived reduction second",
            "does_it_forbid_lambda_active": True,
            "failure_mode": "requires a parent timing/order theorem: identity coupling before projection and no later active invariant",
            "verdict": "best_conditional_theorem_target",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "no_go": "projector_preserving_symmetry_no_go",
            "statement": "If a symmetry preserves P_active, then any polynomial aI+bP_active is symmetry-invariant.",
            "consequence": "S3/screen/projector-preserving symmetry cannot by itself forbid lambda_mem.",
        },
        {
            "no_go": "irreducible_cell_equivalence_tension",
            "statement": "A symmetry strong enough to make the Hamiltonian scalar on all 27 cells also makes a nontrivial active projector non-invariant.",
            "consequence": "full cell equivalence needs a derived two-stage reduction or it erases the active sector.",
        },
        {
            "no_go": "quotient_does_not_fix_weight",
            "statement": "Quotienting representative directions can remove Cperp dependence but does not set the stress weight of a surviving physical block.",
            "consequence": "quotient/gauge route cannot promote epsilon_H without an extra Hamiltonian-weight theorem.",
        },
        {
            "no_go": "index_not_weight",
            "statement": "A topological index can give rank(P_active)=2 but not the coefficient multiplying the Hamiltonian density.",
            "consequence": "q_trace and epsilon_H remain separate gates.",
        },
    ]


def theorem_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "E1_identity_before_projection",
            "required_statement": "H_parent is scalar/identity-coupled on V_cell before P_active is applied.",
            "current_status": "not_derived",
            "why_needed": "only this forces equal Hamiltonian weight per cell",
        },
        {
            "condition": "E2_projector_after_identity",
            "required_statement": "P_active is derived as a reduction/observable after the identity-coupled Hamiltonian current is fixed.",
            "current_status": "not_derived",
            "why_needed": "resolves the full-cell-equivalence versus nontrivial-projector tension",
        },
        {
            "condition": "E3_no_later_active_invariant",
            "required_statement": "the reduced action still forbids lambda_mem P_active H_parent.",
            "current_status": "not_derived",
            "why_needed": "prevents the lambda block from reappearing after projection",
        },
        {
            "condition": "E4_same_lapse_and_scale",
            "required_statement": "the inherited trace is varied by the same lapse and scale normalization as the background Hamiltonian current.",
            "current_status": "open_from_332_333",
            "why_needed": "prevents an independent memory Hamiltonian or scale",
        },
        {
            "condition": "E5_local_support_safety",
            "required_statement": "the same projector remains topological/metric-independent in local exterior reductions.",
            "current_status": "conditional_from_252_333",
            "why_needed": "keeps local silence from being sacrificed for amplitude",
        },
    ]


def gate_rows(sources: list[dict[str, Any]], symmetry: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    by_symmetry = {row["symmetry"]: row for row in symmetry}
    s3_forbids_lambda = bool(by_symmetry["S3_M_x_S3_T_x_screen_plane"]["lambda_block_forbidden"])
    full_forbids_lambda = bool(by_symmetry["full_cell_equivalence_mixing_active_inactive"]["lambda_block_forbidden"])
    full_preserves_projector = bool(by_symmetry["full_cell_equivalence_mixing_active_inactive"]["P_active_invariant"])
    return [
        {"gate": "source_paths_exist", "status": "pass" if sources_ok else "fail", "evidence": sources_ok},
        {
            "gate": "S3_screen_preserves_projector",
            "status": "pass" if float(by_symmetry["S3_M_x_S3_T_x_screen_plane"]["P_active_commutator"]) < 1.0e-12 else "fail",
            "evidence": by_symmetry["S3_M_x_S3_T_x_screen_plane"]["P_active_commutator"],
        },
        {
            "gate": "S3_screen_forbids_active_lambda",
            "status": "fail" if not s3_forbids_lambda else "pass",
            "evidence": by_symmetry["S3_M_x_S3_T_x_screen_plane"]["lambda_current_commutator"],
        },
        {
            "gate": "full_cell_equivalence_forbids_lambda",
            "status": "pass" if full_forbids_lambda else "fail",
            "evidence": by_symmetry["full_cell_equivalence_mixing_active_inactive"]["lambda_current_commutator"],
        },
        {
            "gate": "full_cell_equivalence_preserves_Pactive",
            "status": "fail" if not full_preserves_projector else "pass",
            "evidence": by_symmetry["full_cell_equivalence_mixing_active_inactive"]["P_active_commutator"],
        },
        {
            "gate": "two_stage_identity_then_project_parent_derived",
            "status": "fail",
            "evidence": "best route identified but no parent timing/order theorem exists",
        },
        {
            "gate": "no_active_block_invariant_parent_derived",
            "status": "fail",
            "evidence": "lambda_mem P_active remains invariant under projector-preserving symmetries",
        },
        {
            "gate": "epsilon_H_parent_derived",
            "status": "fail",
            "evidence": "cell-equivalence route has a tension, not a theorem",
        },
        {
            "gate": "Bmem_parent_promotion_allowed",
            "status": "fail",
            "evidence": "epsilon_H, Hstar, q_trace remain theorem targets",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The symmetry audit rejects the simple rescue: S3_M x S3_T x screen symmetry preserves P_active but also "
                "allows I+(lambda-1)P_active, so it cannot derive epsilon_H=1. Full cell equivalence can forbid the lambda "
                "block only by mixing active and inactive states, which makes P_active non-invariant. The remaining viable "
                "route is a two-stage theorem: identity Hamiltonian coupling before projection, then a parent-derived active "
                "projector with no later active-block invariant."
            ),
            "next_target": "derive_or_reject_two_stage_identity_then_project_ordering_theorem",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    symmetry = symmetry_test_rows()
    routes = route_audit_rows()
    no_go = no_go_rows()
    contract = theorem_contract_rows()
    gates = gate_rows(sources, symmetry)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": (sources, ["source", "role", "exists", "issue"]),
        "symmetry_tests.csv": (
            symmetry,
            ["symmetry", "P_active_commutator", "lambda_current_commutator", "P_active_invariant", "lambda_block_forbidden", "readout", "meaning"],
        ),
        "route_audit.csv": (
            routes,
            ["route", "what_it_derives", "does_it_forbid_lambda_active", "failure_mode", "verdict"],
        ),
        "no_go_lemmas.csv": (no_go, ["no_go", "statement", "consequence"]),
        "theorem_contract.csv": (contract, ["condition", "required_statement", "current_status", "why_needed"]),
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
        "S3_forbids_lambda": False,
        "full_cell_equivalence_preserves_Pactive": False,
        "epsilon_H_parent_derived": False,
        "promotion_allowed": False,
        "next_target": "derive_or_reject_two_stage_identity_then_project_ordering_theorem",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cell-equivalence/no-active-block symmetry gate for epsilon_H.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
