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
RUN_SLUG = "no-later-active-counterterm-theorem-gate"
STATUS = "no_later_active_counterterm_not_derived_exact_parent_pullback_contract_identified"
CLAIM_CEILING = "counterterm_gate_no_epsilonH_Bmem_or_parent_action_promotion"
DIM_CELL = 27
RANK_ACTIVE = 2
Q_TRACE = Fraction(RANK_ACTIVE, DIM_CELL)
DELTA_TEST = 0.0061980866083466
LAMBDA_TEST = 1.0 + DELTA_TEST


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


def inactive_projector() -> np.ndarray:
    return np.eye(DIM_CELL) - active_projector()


def active_inactive_swap() -> np.ndarray:
    swap = np.eye(DIM_CELL)
    swap[[0, 2], :] = swap[[2, 0], :]
    return swap


def active_rotation(theta: float = 0.37) -> np.ndarray:
    rotation = np.eye(DIM_CELL)
    cosine = float(np.cos(theta))
    sine = float(np.sin(theta))
    rotation[0:2, 0:2] = np.array([[cosine, -sine], [sine, cosine]])
    return rotation


def inactive_swap() -> np.ndarray:
    swap = np.eye(DIM_CELL)
    swap[[2, 3], :] = swap[[3, 2], :]
    return swap


def full_equivalence_generators() -> list[np.ndarray]:
    return [active_inactive_swap()]


def residual_projector_preserving_generators() -> list[np.ndarray]:
    return [active_rotation(), inactive_swap(), active_projector(), inactive_projector()]


def max_commutator_norm(operator: np.ndarray, generators: list[np.ndarray]) -> float:
    if not generators:
        return 0.0
    return max(float(np.linalg.norm(operator @ generator - generator @ operator)) for generator in generators)


def epsilon_from_current(current: np.ndarray) -> float:
    projector = active_projector()
    active_trace = float(np.trace(projector @ current))
    return active_trace / RANK_ACTIVE


def full_trace_average(current: np.ndarray) -> float:
    return float(np.trace(current)) / DIM_CELL


def q_trace_from_current(current: np.ndarray) -> float:
    projector = active_projector()
    return float(np.trace(projector @ current)) / DIM_CELL


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "331-trace-normalized-Hamiltonian-amplitude-contract.md", "B_mem trace factorization"),
        (ROOT / "332-parent-Hamiltonian-trace-current-gate.md", "Hamiltonian trace-current amplitude gate"),
        (ROOT / "333-literal-projected-Hamiltonian-subblock-gate.md", "literal projected subblock counterexamples"),
        (ROOT / "334-cell-equivalence-no-active-block-symmetry-gate.md", "full-cell versus active-block symmetry gate"),
        (ROOT / "335-two-stage-identity-then-project-ordering-gate.md", "two-stage ordering gate"),
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


def operator_rows() -> list[dict[str, Any]]:
    identity = np.eye(DIM_CELL)
    projector = active_projector()
    inactive = inactive_projector()
    lambda_current = identity + DELTA_TEST * projector
    trace_compensated = identity + DELTA_TEST * projector - DELTA_TEST * (RANK_ACTIVE / (DIM_CELL - RANK_ACTIVE)) * inactive
    active_only = projector
    full_generators = full_equivalence_generators()
    residual_generators = residual_projector_preserving_generators()
    candidates = [
        ("identity_parent_current", identity, "allowed by full cell equivalence and residual symmetry"),
        ("lambda_active_counterterm", lambda_current, "forbidden by full equivalence but allowed after projection"),
        ("trace_compensated_lambda_counterterm", trace_compensated, "keeps total trace fixed while shifting active amplitude"),
        ("active_only_projector_current", active_only, "gets active trace right by insertion, not inheritance"),
    ]
    rows: list[dict[str, Any]] = []
    for name, current, meaning in candidates:
        rows.append(
            {
                "operator": name,
                "epsilon_H": epsilon_from_current(current),
                "q_trace_effective": q_trace_from_current(current),
                "full_trace_average": full_trace_average(current),
                "full_equivalence_commutator": max_commutator_norm(current, full_generators),
                "residual_commutator": max_commutator_norm(current, residual_generators),
                "meaning": meaning,
            }
        )
    return rows


def route_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "residual_projector_preserving_symmetry",
            "test": "after P_active exists, require invariance under block-preserving residual transformations",
            "result": "fails_to_forbid_counterterm",
            "reason": "the invariant algebra contains span(P_active, I-P_active), so lambda_mem P_active is allowed",
            "status": "fail",
        },
        {
            "route": "full_cell_equivalence_same_stage",
            "test": "require invariance under transformations that exchange active and inactive cells",
            "result": "forbids_counterterm_but_also_forbids_nontrivial_projector",
            "reason": "P_active does not commute with active-inactive exchange, so this cannot be the same stage as the physical projection",
            "status": "fail_as_full_derivation",
        },
        {
            "route": "topological_rank_index",
            "test": "fix rank(P_active)=2 and dim(V_cell)=27",
            "result": "fixes_support_not_weight",
            "reason": "rank fixes q_trace=2/27 only for identity current; P_active-weighted currents shift the amplitude",
            "status": "fail",
        },
        {
            "route": "total_trace_normalization",
            "test": "fix Tr(H_parent)/27=1",
            "result": "does_not_fix_active_trace",
            "reason": "active and inactive weights can compensate while preserving total trace",
            "status": "fail",
        },
        {
            "route": "gauge_quotient_lambda",
            "test": "declare lambda_mem P_active to be a pure representative choice",
            "result": "not_a_gauge_if_B_mem_is_observable",
            "reason": "changing lambda changes epsilon_H and therefore changes the projected memory amplitude",
            "status": "fail",
        },
        {
            "route": "first_class_constraint_closure",
            "test": "use Hamiltonian/Dirac closure to select lambda_mem=1",
            "result": "closure_is_rescaling_blind",
            "reason": "a nonzero scaling of a separately allowed reduced invariant preserves first-class closure unless normalization is parent-owned",
            "status": "fail",
        },
        {
            "route": "technical_naturalness",
            "test": "argue lambda_mem=1 is stable",
            "result": "not_a_derivation",
            "reason": "stability near one is weaker than selecting exactly one, and residual symmetry does not make lambda=1 enhanced",
            "status": "fail",
        },
        {
            "route": "exact_parent_pullback_no_new_reduced_invariants",
            "test": "allow only reduced terms that lift to full-cell-equivalence invariants before projection",
            "result": "sufficient_if_imposed",
            "reason": "lambda_mem P_active is residual-invariant but has no full-cell-invariant lift",
            "status": "conditional_contract",
        },
    ]


def constraint_test_rows(operators: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_operator = {row["operator"]: row for row in operators}
    trace_compensated = by_operator["trace_compensated_lambda_counterterm"]
    lambda_counterterm = by_operator["lambda_active_counterterm"]
    return [
        {
            "constraint": "residual_invariance",
            "diagnostic": "commutator(lambda_active_counterterm, residual_generators)",
            "value": lambda_counterterm["residual_commutator"],
            "verdict": "counterterm_allowed",
        },
        {
            "constraint": "full_cell_invariance",
            "diagnostic": "commutator(lambda_active_counterterm, active_inactive_swap)",
            "value": lambda_counterterm["full_equivalence_commutator"],
            "verdict": "counterterm_forbidden_only_before_projection",
        },
        {
            "constraint": "fixed_total_trace",
            "diagnostic": "trace_compensated_lambda_counterterm full_trace_average",
            "value": trace_compensated["full_trace_average"],
            "verdict": "total_trace_fixed_but_active_amplitude_moves",
        },
        {
            "constraint": "projected_amplitude_gauge_test",
            "diagnostic": "d epsilon_H / d lambda_mem",
            "value": 1.0,
            "verdict": "not_pure_gauge_if_projected_amplitude_is_physical",
        },
        {
            "constraint": "topological_rank_test",
            "diagnostic": "rank fixes q_trace for identity current only",
            "value": f"{Q_TRACE.numerator}/{Q_TRACE.denominator}",
            "verdict": "rank_does_not_fix_weighted_current",
        },
    ]


def exact_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "C1_parent_operator_algebra",
            "required_statement": "before projection, allowed Hamiltonian-current operators are generated by full-cell-equivalence invariants",
            "effect_if_true": "fixes H_parent proportional to I_cell",
            "current_status": "not_yet_parent_derived",
        },
        {
            "condition": "C2_projection_is_readout_not_new_EFT",
            "required_statement": "P_active is a reduction/readout map, not permission to write a new residual-invariant action",
            "effect_if_true": "prevents lambda_mem P_active from entering as an independent reduced coupling",
            "current_status": "not_yet_parent_derived",
        },
        {
            "condition": "C3_pullback_selection_rule",
            "required_statement": "every reduced counterterm must lift to a full-cell-equivalence invariant before projection",
            "effect_if_true": "rejects P_active counterterms because they do not lift to the full stage",
            "current_status": "mathematically_sufficient_if_imposed",
        },
        {
            "condition": "C4_same_constraint_current",
            "required_statement": "the projected trace is a subtrace of the same lapse/Hamiltonian constraint current",
            "effect_if_true": "blocks independent reduced-sector normalization",
            "current_status": "open",
        },
        {
            "condition": "C5_no_quantum_or_effective_reopening",
            "required_statement": "radiative/effective corrections obey the same pullback selection rule",
            "effect_if_true": "keeps lambda_mem from reappearing in the effective action",
            "current_status": "open",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma": "residual_invariant_counterterm_lemma",
            "statement": "Given nonzero P_active and residual symmetries that preserve its active/inactive split, P_active itself is an invariant tensor.",
            "consequence": "a reduced action respecting only residual symmetry may contain lambda_mem P_active.",
        },
        {
            "lemma": "rank_weight_separation_lemma",
            "statement": "rank(P_active)=2 fixes the support count but not the Hamiltonian weight carried by that support.",
            "consequence": "q_trace=2/27 is derived only for identity weighting, not for arbitrary active-block weighting.",
        },
        {
            "lemma": "total_trace_blindness_lemma",
            "statement": "Tr(H_parent) can stay fixed while active and inactive block weights vary oppositely.",
            "consequence": "global normalization cannot by itself select epsilon_H=1.",
        },
        {
            "lemma": "quotient_or_EFT_fork",
            "statement": "An exact parent pullback forbids non-liftable reduced terms, while a Wilsonian reduced EFT allows all residual invariants.",
            "consequence": "the amplitude derivation now depends on which fork the parent action proves.",
        },
    ]


def gate_rows(sources: list[dict[str, Any]], operators: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    by_operator = {row["operator"]: row for row in operators}
    lambda_counterterm = by_operator["lambda_active_counterterm"]
    trace_compensated = by_operator["trace_compensated_lambda_counterterm"]
    return [
        {"gate": "source_paths_exist", "status": "pass" if sources_ok else "fail", "evidence": sources_ok},
        {
            "gate": "residual_symmetry_forbids_lambda",
            "status": "fail",
            "evidence": lambda_counterterm["residual_commutator"],
        },
        {
            "gate": "full_equivalence_forbids_lambda_same_stage",
            "status": "pass" if float(lambda_counterterm["full_equivalence_commutator"]) > 1.0e-12 else "fail",
            "evidence": lambda_counterterm["full_equivalence_commutator"],
        },
        {
            "gate": "topological_rank_fixes_weight",
            "status": "fail",
            "evidence": "rank fixes 2/27 support but lambda changes epsilon_H",
        },
        {
            "gate": "total_trace_normalization_fixes_active_weight",
            "status": "fail" if abs(float(trace_compensated["full_trace_average"]) - 1.0) < 1.0e-12 else "pass",
            "evidence": f"full_trace_average={trace_compensated['full_trace_average']}; epsilon_H={trace_compensated['epsilon_H']}",
        },
        {
            "gate": "gauge_quotient_removes_lambda",
            "status": "fail",
            "evidence": "epsilon_H changes with lambda_mem",
        },
        {
            "gate": "exact_parent_pullback_sufficient_if_imposed",
            "status": "pass",
            "evidence": "lambda_mem P_active is residual-invariant but not full-cell-invariant",
        },
        {
            "gate": "exact_parent_pullback_parent_derived",
            "status": "fail",
            "evidence": "no current parent action proves no new reduced invariants",
        },
        {
            "gate": "no_later_active_counterterm_parent_derived",
            "status": "fail",
            "evidence": "counterterm is forbidden only under an added exact-pullback selection rule",
        },
        {
            "gate": "epsilon_H_parent_derived",
            "status": "fail",
            "evidence": "epsilon_H=1 follows conditionally, not unconditionally",
        },
        {
            "gate": "closure_contract_available",
            "status": "pass",
            "evidence": "C1-C5 exact parent pullback contract written",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The no-later-active-counterterm theorem is not derived from residual symmetry, topology, trace normalization, "
                "gauge quotient, first-class closure, or naturalness. The exact parent-pullback rule would be sufficient: "
                "only operators that lift to full-cell-equivalence invariants before projection are allowed after projection. "
                "But that rule is currently a parent-action contract, not an established theorem."
            ),
            "next_target": "derive_parent_exact_pullback_selection_rule_or_keep_epsilonH_as_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    operators = operator_rows()
    routes = route_audit_rows()
    constraints = constraint_test_rows(operators)
    contract = exact_contract_rows()
    no_gos = no_go_rows()
    gates = gate_rows(sources, operators)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": (sources, ["source", "role", "exists", "issue"]),
        "operator_counterexamples.csv": (
            operators,
            [
                "operator",
                "epsilon_H",
                "q_trace_effective",
                "full_trace_average",
                "full_equivalence_commutator",
                "residual_commutator",
                "meaning",
            ],
        ),
        "route_audit.csv": (routes, ["route", "test", "result", "reason", "status"]),
        "constraint_tests.csv": (constraints, ["constraint", "diagnostic", "value", "verdict"]),
        "exact_parent_pullback_contract.csv": (
            contract,
            ["condition", "required_statement", "effect_if_true", "current_status"],
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
        "lambda_test": LAMBDA_TEST,
        "no_later_counterterm_derived": False,
        "epsilon_H_parent_derived": False,
        "exact_parent_pullback_sufficient": True,
        "exact_parent_pullback_parent_derived": False,
        "promotion_allowed": False,
        "next_target": "derive_parent_exact_pullback_selection_rule_or_keep_epsilonH_as_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="No-later-active-counterterm theorem gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
