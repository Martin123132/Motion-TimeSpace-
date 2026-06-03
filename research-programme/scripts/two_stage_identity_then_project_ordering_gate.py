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
RUN_SLUG = "two-stage-identity-then-project-ordering-gate"
STATUS = "two_stage_identity_then_project_template_conditional_post_projection_lambda_not_forbidden"
CLAIM_CEILING = "ordering_template_only_no_epsilonH_Bmem_or_parent_action_promotion"
DIM_CELL = 27
RANK_ACTIVE = 2
Q_TRACE = Fraction(RANK_ACTIVE, DIM_CELL)
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


def active_projector() -> np.ndarray:
    projector = np.zeros((DIM_CELL, DIM_CELL), dtype=float)
    projector[0, 0] = 1.0
    projector[1, 1] = 1.0
    return projector


def active_inactive_swap() -> np.ndarray:
    swap = np.eye(DIM_CELL)
    swap[[0, 2], :] = swap[[2, 0], :]
    return swap


def full_equivalence_generators() -> list[np.ndarray]:
    return [active_inactive_swap()]


def residual_projector_preserving_generators() -> list[np.ndarray]:
    projector = active_projector()
    return [projector, np.eye(DIM_CELL) - projector]


def max_commutator_norm(operator: np.ndarray, generators: list[np.ndarray]) -> float:
    if not generators:
        return 0.0
    return max(float(np.linalg.norm(operator @ generator - generator @ operator)) for generator in generators)


def epsilon_from_current(current: np.ndarray) -> float:
    projector = active_projector()
    active_trace = float(np.trace(projector @ current))
    return active_trace / RANK_ACTIVE


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "333-literal-projected-Hamiltonian-subblock-gate.md", "literal subblock template"),
        (ROOT / "334-cell-equivalence-no-active-block-symmetry-gate.md", "cell-equivalence/no-active-block symmetry audit"),
        (ROOT / "332-parent-Hamiltonian-trace-current-gate.md", "Hamiltonian trace-current contract"),
        (ROOT / "260-C3-unit-stress-normalization-parent-action-attempt.md", "C3 stress-form split"),
        (ROOT / "252-topological-projector-parent-action-skeleton.md", "projector local-silence skeleton"),
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


def ordering_case_rows() -> list[dict[str, Any]]:
    identity = np.eye(DIM_CELL)
    projector = active_projector()
    lambda_current = identity + (LAMBDA_TEST - 1.0) * projector
    active_only_current = projector
    full_generators = full_equivalence_generators()
    residual_generators = residual_projector_preserving_generators()
    cases = [
        {
            "case": "project_first_under_full_cell_equivalence",
            "stage_1": "P_active introduced while full cell equivalence is still active",
            "stage_2": "try to keep full identity coupling",
            "current": identity,
            "projector_full_commutator": max_commutator_norm(projector, full_generators),
            "current_full_commutator": max_commutator_norm(identity, full_generators),
            "current_residual_commutator": max_commutator_norm(identity, residual_generators),
            "epsilon_H": epsilon_from_current(identity),
            "readout": "fails_projector_invariance",
            "meaning": "Full equivalence fixes identity coupling but does not allow a nontrivial active projector at the same stage.",
        },
        {
            "case": "identity_then_project_no_counterterm",
            "stage_1": "full cell equivalence fixes H_parent=I_cell",
            "stage_2": "P_active is derived after symmetry reduction",
            "current": identity,
            "projector_full_commutator": max_commutator_norm(projector, full_generators),
            "current_full_commutator": max_commutator_norm(identity, full_generators),
            "current_residual_commutator": max_commutator_norm(identity, residual_generators),
            "epsilon_H": epsilon_from_current(identity),
            "readout": "conditional_template_pass",
            "meaning": "This is the desired ordering: unit weight is fixed before projection, and no later active counterterm is added.",
        },
        {
            "case": "identity_then_project_plus_lambda_counterterm",
            "stage_1": "full cell equivalence fixes H_parent=I_cell",
            "stage_2": "P_active is derived, then a reduced invariant lambda_mem P_active is allowed",
            "current": lambda_current,
            "projector_full_commutator": max_commutator_norm(projector, full_generators),
            "current_full_commutator": max_commutator_norm(lambda_current, full_generators),
            "current_residual_commutator": max_commutator_norm(lambda_current, residual_generators),
            "epsilon_H": epsilon_from_current(lambda_current),
            "readout": "post_projection_lambda_reopens_amplitude",
            "meaning": "After projection, the residual projector-preserving algebra allows lambda_mem unless a no-later-invariant theorem forbids it.",
        },
        {
            "case": "active_only_inserted_after_identity",
            "stage_1": "identity coupling is discarded after reduction",
            "stage_2": "H_parent=P_active H_scale is used as the memory current",
            "current": active_only_current,
            "projector_full_commutator": max_commutator_norm(projector, full_generators),
            "current_full_commutator": max_commutator_norm(active_only_current, full_generators),
            "current_residual_commutator": max_commutator_norm(active_only_current, residual_generators),
            "epsilon_H": epsilon_from_current(active_only_current),
            "readout": "imposition_not_inheritance",
            "meaning": "The number survives only because the active block was inserted as the parent current.",
        },
    ]
    rows: list[dict[str, Any]] = []
    for case in cases:
        rows.append(
            {
                "case": case["case"],
                "stage_1": case["stage_1"],
                "stage_2": case["stage_2"],
                "epsilon_H": case["epsilon_H"],
                "projector_full_commutator": case["projector_full_commutator"],
                "current_full_commutator": case["current_full_commutator"],
                "current_residual_commutator": case["current_residual_commutator"],
                "readout": case["readout"],
                "meaning": case["meaning"],
            }
        )
    return rows


def ordering_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "O1_full_equivalence_stage",
            "required_statement": "before active projection, the parent Hamiltonian current is fixed to H_parent proportional to I_cell",
            "current_status": "template_only",
            "why_needed": "this is what fixes equal cell weights",
        },
        {
            "condition": "O2_projection_as_reduction",
            "required_statement": "P_active appears only after O1 as a derived reduction/observable, not as a same-stage invariant",
            "current_status": "not_parent_derived",
            "why_needed": "avoids the full-equivalence/nontrivial-projector contradiction",
        },
        {
            "condition": "O3_no_reduced_counterterm",
            "required_statement": "the reduced theory forbids lambda_mem P_active H_parent after projection",
            "current_status": "missing_core_theorem",
            "why_needed": "otherwise post-projection lambda reopens kappa_mem",
        },
        {
            "condition": "O4_same_lapse_survives_reduction",
            "required_statement": "the projected trace remains a subblock of the same lapse Hamiltonian constraint",
            "current_status": "open",
            "why_needed": "prevents independent reduced-sector Hamiltonian normalization",
        },
        {
            "condition": "O5_local_support_survives_reduction",
            "required_statement": "the reduction preserves the topological/local projector-stress silence route",
            "current_status": "conditional_from_prior_gates",
            "why_needed": "keeps amplitude route compatible with local-GR branch",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "no_go": "same_stage_no_go",
            "statement": "Full cell equivalence and nontrivial P_active cannot both be exact same-stage symmetries.",
            "consequence": "project-first under full equivalence fails.",
        },
        {
            "no_go": "post_projection_counterterm_no_go",
            "statement": "After P_active exists, lambda_mem P_active is invariant under the residual projector-preserving algebra.",
            "consequence": "identity-first alone does not forbid later amplitude freedom.",
        },
        {
            "no_go": "active_only_not_inheritance",
            "statement": "Using H_parent=P_active H_scale gets the trace right by inserting the desired block as the parent current.",
            "consequence": "this is closure unless a parent reduction theorem forces it.",
        },
        {
            "no_go": "ordering_is_dynamical_not_notational",
            "statement": "The word 'then' must be a parent variational or constraint statement, not prose order.",
            "consequence": "two-stage route remains a theorem target until the action owns the ordering.",
        },
    ]


def gate_rows(sources: list[dict[str, Any]], cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    by_case = {row["case"]: row for row in cases}
    clean = by_case["identity_then_project_no_counterterm"]
    post_lambda = by_case["identity_then_project_plus_lambda_counterterm"]
    project_first = by_case["project_first_under_full_cell_equivalence"]
    return [
        {"gate": "source_paths_exist", "status": "pass" if sources_ok else "fail", "evidence": sources_ok},
        {
            "gate": "identity_then_project_template_gives_unit_epsilon",
            "status": "pass" if abs(float(clean["epsilon_H"]) - 1.0) < 1.0e-12 else "fail",
            "evidence": clean["epsilon_H"],
        },
        {
            "gate": "project_first_same_stage_fails",
            "status": "pass" if float(project_first["projector_full_commutator"]) > 1.0e-12 else "fail",
            "evidence": project_first["projector_full_commutator"],
        },
        {
            "gate": "post_projection_lambda_counterexample",
            "status": "pass" if abs(float(post_lambda["epsilon_H"]) - 1.0) > 1.0e-6 else "fail",
            "evidence": post_lambda["epsilon_H"],
        },
        {
            "gate": "post_projection_lambda_residual_invariant",
            "status": "pass" if float(post_lambda["current_residual_commutator"]) < 1.0e-12 else "fail",
            "evidence": post_lambda["current_residual_commutator"],
        },
        {
            "gate": "ordering_parent_derived",
            "status": "fail",
            "evidence": "no variational/constraint theorem currently enforces identity-before-projection",
        },
        {
            "gate": "no_later_active_counterterm_parent_derived",
            "status": "fail",
            "evidence": "lambda_mem P_active remains a residual invariant after projection",
        },
        {
            "gate": "epsilon_H_parent_derived",
            "status": "fail",
            "evidence": "conditional ordering template only",
        },
        {
            "gate": "Bmem_parent_promotion_allowed",
            "status": "fail",
            "evidence": "epsilon_H/Hstar/q_trace still theorem targets",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The two-stage ordering template works only in the clean no-counterterm case: full cell equivalence first fixes "
                "identity coupling, then P_active projection gives epsilon_H=1. But this is not a derivation because project-first "
                "fails same-stage symmetry and post-projection lambda_mem P_active is a residual invariant unless a new parent "
                "no-counterterm theorem forbids it."
            ),
            "next_target": "derive_or_demote_no_later_active_counterterm_theorem",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    cases = ordering_case_rows()
    contract = ordering_contract_rows()
    no_go = no_go_rows()
    gates = gate_rows(sources, cases)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": (sources, ["source", "role", "exists", "issue"]),
        "ordering_cases.csv": (
            cases,
            [
                "case",
                "stage_1",
                "stage_2",
                "epsilon_H",
                "projector_full_commutator",
                "current_full_commutator",
                "current_residual_commutator",
                "readout",
                "meaning",
            ],
        ),
        "ordering_contract.csv": (contract, ["condition", "required_statement", "current_status", "why_needed"]),
        "no_go_lemmas.csv": (no_go, ["no_go", "statement", "consequence"]),
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
        "q_trace": f"{Q_TRACE.numerator}/{Q_TRACE.denominator}",
        "two_stage_template_constructed": True,
        "ordering_parent_derived": False,
        "no_later_counterterm_derived": False,
        "epsilon_H_parent_derived": False,
        "promotion_allowed": False,
        "next_target": "derive_or_demote_no_later_active_counterterm_theorem",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Two-stage identity-then-project ordering theorem gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
