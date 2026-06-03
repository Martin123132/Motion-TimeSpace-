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
RUN_SLUG = "action-level-exact-readout-gate"
STATUS = "action_level_exact_readout_contract_constructed_Pactive_probe_premise_open"
CLAIM_CEILING = "action_readout_contract_no_unconditional_epsilonH_Bmem_or_parent_action_promotion"
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


def active_mask() -> np.ndarray:
    mask = np.zeros(DIM_CELL, dtype=float)
    mask[:RANK_ACTIVE] = 1.0
    return mask


def inactive_mask() -> np.ndarray:
    return 1.0 - active_mask()


def epsilon_from_weights(weights: np.ndarray) -> float:
    return float(np.dot(active_mask(), weights) / RANK_ACTIVE)


def q_trace_from_weights(weights: np.ndarray) -> float:
    return float(np.dot(active_mask(), weights) / DIM_CELL)


def full_average(weights: np.ndarray) -> float:
    return float(np.mean(weights))


def full_symmetry_violation(weights: np.ndarray) -> float:
    return float(np.max(weights) - np.min(weights))


def residual_symmetry_violation(weights: np.ndarray) -> float:
    active = weights[:RANK_ACTIVE]
    inactive = weights[RANK_ACTIVE:]
    return float(max(np.max(active) - np.min(active), np.max(inactive) - np.min(inactive)))


def parent_solution(source_strength: float = 0.0, source_is_physical: bool = False) -> np.ndarray:
    """Finite witness for S=1/2 sum_i (h_i-1)^2 - J sum_active h_i.

    If the source is a probe, physical equations are evaluated at J=0.
    If the source is physical, active cells shift by J.
    """
    weights = np.ones(DIM_CELL, dtype=float)
    if source_is_physical:
        weights += source_strength * active_mask()
    return weights


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "335-two-stage-identity-then-project-ordering-gate.md", "ordering versus counterterm burden"),
        (ROOT / "336-no-later-active-counterterm-theorem-gate.md", "no-later-counterterm route audit"),
        (ROOT / "337-exact-parent-pullback-selection-rule-gate.md", "conditional exact-pullback theorem"),
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


def action_scenario_rows() -> list[dict[str, Any]]:
    exact_readout = parent_solution()
    probe_source = parent_solution(source_strength=DELTA_TEST, source_is_physical=False)
    physical_spurion = parent_solution(source_strength=DELTA_TEST, source_is_physical=True)
    trace_compensated_spurion = np.ones(DIM_CELL, dtype=float)
    trace_compensated_spurion += DELTA_TEST * active_mask()
    trace_compensated_spurion -= DELTA_TEST * RANK_ACTIVE / (DIM_CELL - RANK_ACTIVE) * inactive_mask()
    scenarios = [
        {
            "scenario": "parent_action_then_observable_readout",
            "action_contains_Pactive": False,
            "variation_order": "vary S_parent first; apply P_active only to the solved current",
            "weights": exact_readout,
            "counterterm_allowed_by_rule": False,
            "verdict": "conditional_exact_readout_pass",
        },
        {
            "scenario": "probe_source_differentiated_at_zero",
            "action_contains_Pactive": "source_only",
            "variation_order": "use J P_active only as a generating-source insertion, set J=0 for physical equations",
            "weights": probe_source,
            "counterterm_allowed_by_rule": False,
            "verdict": "probe_does_not_shift_background",
        },
        {
            "scenario": "physical_Pactive_spurion_in_action",
            "action_contains_Pactive": True,
            "variation_order": "P_active is present in the physical reduced action",
            "weights": physical_spurion,
            "counterterm_allowed_by_rule": True,
            "verdict": "counterterm_reopens_amplitude",
        },
        {
            "scenario": "trace_compensated_physical_spurion",
            "action_contains_Pactive": True,
            "variation_order": "active shift is compensated by inactive shift to keep full trace fixed",
            "weights": trace_compensated_spurion,
            "counterterm_allowed_by_rule": True,
            "verdict": "trace_normalization_still_not_enough",
        },
    ]
    rows: list[dict[str, Any]] = []
    for scenario in scenarios:
        weights = scenario["weights"]
        rows.append(
            {
                "scenario": scenario["scenario"],
                "action_contains_Pactive": scenario["action_contains_Pactive"],
                "variation_order": scenario["variation_order"],
                "epsilon_H": epsilon_from_weights(weights),
                "q_trace_effective": q_trace_from_weights(weights),
                "full_trace_average": full_average(weights),
                "full_symmetry_violation": full_symmetry_violation(weights),
                "residual_symmetry_violation": residual_symmetry_violation(weights),
                "counterterm_allowed_by_rule": scenario["counterterm_allowed_by_rule"],
                "verdict": scenario["verdict"],
            }
        )
    return rows


def source_probe_rows() -> list[dict[str, Any]]:
    j_values = [0.0, DELTA_TEST, -DELTA_TEST]
    rows: list[dict[str, Any]] = []
    for source_strength in j_values:
        probe_weights = parent_solution(source_strength=source_strength, source_is_physical=False)
        physical_weights = parent_solution(source_strength=source_strength, source_is_physical=True)
        rows.append(
            {
                "J_active": source_strength,
                "probe_source_epsilon_H": epsilon_from_weights(probe_weights),
                "probe_source_meaning": "J is used only to differentiate an observable and is set to zero in the physical action",
                "physical_spurion_epsilon_H": epsilon_from_weights(physical_weights),
                "physical_spurion_meaning": "J is a real reduced-action coupling and shifts the active sector",
            }
        )
    return rows


def action_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "A1_parent_variation_before_projection",
            "required_statement": "Euler-Lagrange/constraint equations are derived from S_parent before P_active is applied",
            "effect_if_true": "prevents P_active from changing the physical equations",
            "current_status": "contract_constructed",
        },
        {
            "condition": "A2_Pactive_observable_not_spurion",
            "required_statement": "P_active is only an observable/source-at-zero readout, not a tensor in the physical action",
            "effect_if_true": "forbids lambda_mem P_active as a physical coupling",
            "current_status": "not_yet_parent_derived",
        },
        {
            "condition": "A3_no_independent_S_reduced",
            "required_statement": "there is no separate reduced action S_reduced[P_active] with all residual invariants",
            "effect_if_true": "blocks Wilsonian reintroduction of the active counterterm",
            "current_status": "not_yet_parent_derived",
        },
        {
            "condition": "A4_effective_corrections_are_parent_pullbacks",
            "required_statement": "loops/coarse-graining/corrections preserve the full-parent pullback selection rule",
            "effect_if_true": "keeps counterterms from returning beyond tree level",
            "current_status": "open",
        },
        {
            "condition": "A5_physical_marking_is_boundary_readout",
            "required_statement": "the rank-2 active mark is a boundary/measurement/readout label, not a symmetry-breaking material defect",
            "effect_if_true": "lets P_active be observable while not becoming an action spurion",
            "current_status": "open",
        },
        {
            "condition": "A6_same_lapse_constraint_current",
            "required_statement": "the readout is a subtrace of the same Hamiltonian/lapse current used by the parent action",
            "effect_if_true": "prevents independent normalization of the readout sector",
            "current_status": "open",
        },
    ]


def fork_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "fork": "strict_parent_observable_readout",
            "definition": "P_active appears only in O_active[Phi]=Tr(P_active H_parent[Phi]) after solving or as a source differentiated at zero",
            "counterterm_status": "forbidden_by_construction",
            "epsilon_H_status": "conditional_theorem",
            "risk": "must justify why physical active marking is not an action spurion",
        },
        {
            "fork": "boundary_or_defect_action",
            "definition": "P_active marks a physical boundary/defect term inside the action",
            "counterterm_status": "allowed",
            "epsilon_H_status": "closure_or_fitted",
            "risk": "active counterterm is symmetry-legal and changes the amplitude",
        },
        {
            "fork": "Wilsonian_effective_reduction",
            "definition": "inactive/fast variables are integrated out and the reduced action contains all residual invariants",
            "counterterm_status": "allowed",
            "epsilon_H_status": "closure_or_fitted",
            "risk": "standard EFT logic reopens lambda_mem P_active",
        },
        {
            "fork": "constrained_effective_pullback",
            "definition": "effective corrections exist but must be parent-invariant pullbacks by a Ward/BRST/constraint identity",
            "counterterm_status": "forbidden_if_identity_proved",
            "epsilon_H_status": "possible_theorem",
            "risk": "the required Ward/constraint identity is not yet supplied",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma": "source_spurion_distinction",
            "statement": "A source used to differentiate an observable at J=0 does not alter the physical equations; a physical spurion in the action does.",
            "consequence": "P_active must be a probe/readout, not a physical coupling, for the counterterm to stay forbidden.",
        },
        {
            "lemma": "boundary_defect_counterterm_hazard",
            "statement": "If the active mark is a real boundary/defect in the action, residual symmetry permits active-local terms.",
            "consequence": "the exact-readout theorem fails unless boundary terms are fixed by an additional principle.",
        },
        {
            "lemma": "EFT_reduction_hazard",
            "statement": "Integrating out degrees of freedom usually generates every operator allowed by residual symmetry.",
            "consequence": "standard reduced EFT logic demotes epsilon_H to a coupling unless a parent Ward/constraint identity forbids it.",
        },
        {
            "lemma": "action_ownership_burden",
            "statement": "A readout rule is a theorem only when the action specifies that projection is post-variation and non-dynamical.",
            "consequence": "exact readout is now an action principle target, not merely algebraic preference.",
        },
    ]


def gate_rows(sources: list[dict[str, Any]], scenarios: list[dict[str, Any]], probes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    by_scenario = {row["scenario"]: row for row in scenarios}
    exact = by_scenario["parent_action_then_observable_readout"]
    physical = by_scenario["physical_Pactive_spurion_in_action"]
    trace_comp = by_scenario["trace_compensated_physical_spurion"]
    probe_shift = next(row for row in probes if abs(float(row["J_active"]) - DELTA_TEST) < 1.0e-15)
    return [
        {"gate": "source_paths_exist", "status": "pass" if sources_ok else "fail", "evidence": sources_ok},
        {
            "gate": "post_variation_observable_readout_gives_epsilon_one",
            "status": "pass" if abs(float(exact["epsilon_H"]) - 1.0) < 1.0e-12 else "fail",
            "evidence": exact["epsilon_H"],
        },
        {
            "gate": "post_variation_observable_readout_gives_q_trace_2over27",
            "status": "pass" if abs(float(exact["q_trace_effective"]) - float(Q_TRACE)) < 1.0e-12 else "fail",
            "evidence": exact["q_trace_effective"],
        },
        {
            "gate": "source_at_zero_does_not_shift_background",
            "status": "pass" if abs(float(probe_shift["probe_source_epsilon_H"]) - 1.0) < 1.0e-12 else "fail",
            "evidence": probe_shift["probe_source_epsilon_H"],
        },
        {
            "gate": "physical_Pactive_spurion_shifts_epsilon",
            "status": "pass" if abs(float(physical["epsilon_H"]) - 1.0) > 1.0e-6 else "fail",
            "evidence": physical["epsilon_H"],
        },
        {
            "gate": "trace_compensated_spurion_still_shifts_epsilon",
            "status": "pass" if abs(float(trace_comp["full_trace_average"]) - 1.0) < 1.0e-12 and abs(float(trace_comp["epsilon_H"]) - 1.0) > 1.0e-6 else "fail",
            "evidence": f"full_trace_average={trace_comp['full_trace_average']}; epsilon_H={trace_comp['epsilon_H']}",
        },
        {
            "gate": "action_level_exact_readout_sufficient",
            "status": "pass",
            "evidence": "A1-A6 forbid P_active as a physical action spurion if imposed",
        },
        {
            "gate": "parent_action_currently_proves_Pactive_probe_not_spurion",
            "status": "fail",
            "evidence": "current branch has a contract but not a parent variational derivation",
        },
        {
            "gate": "effective_corrections_proven_parent_pullback",
            "status": "fail",
            "evidence": "no Ward/BRST/constraint identity has been supplied for correction terms",
        },
        {
            "gate": "epsilon_H_parent_derived_unconditionally",
            "status": "fail",
            "evidence": "depends on action-level exact-readout premises",
        },
        {
            "gate": "Bmem_parent_promotion_allowed",
            "status": "fail",
            "evidence": "exact readout, Hstar=H0, and correction stability remain open",
        },
        {
            "gate": "closure_contract_available",
            "status": "pass",
            "evidence": "action-level readout contract A1-A6 written",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The action-level route is viable only if P_active is a post-variation observable/source-at-zero readout. "
                "In that strict branch, the active counterterm is not part of the physical action and epsilon_H=1 remains "
                "a conditional theorem. If P_active is a physical boundary/defect spurion or if a reduced Wilsonian EFT is "
                "introduced, lambda_mem P_active is allowed and epsilon_H becomes a closure/fitted coupling."
            ),
            "next_target": "derive_Pactive_as_boundary_observable_not_action_spurion_or_freeze_epsilonH_as_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    scenarios = action_scenario_rows()
    probes = source_probe_rows()
    contract = action_contract_rows()
    forks = fork_audit_rows()
    no_gos = no_go_rows()
    gates = gate_rows(sources, scenarios, probes)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": (sources, ["source", "role", "exists", "issue"]),
        "action_scenarios.csv": (
            scenarios,
            [
                "scenario",
                "action_contains_Pactive",
                "variation_order",
                "epsilon_H",
                "q_trace_effective",
                "full_trace_average",
                "full_symmetry_violation",
                "residual_symmetry_violation",
                "counterterm_allowed_by_rule",
                "verdict",
            ],
        ),
        "source_probe_vs_spurion.csv": (
            probes,
            [
                "J_active",
                "probe_source_epsilon_H",
                "probe_source_meaning",
                "physical_spurion_epsilon_H",
                "physical_spurion_meaning",
            ],
        ),
        "action_readout_contract.csv": (
            contract,
            ["condition", "required_statement", "effect_if_true", "current_status"],
        ),
        "fork_audit.csv": (
            forks,
            ["fork", "definition", "counterterm_status", "epsilon_H_status", "risk"],
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
        "action_level_exact_readout_contract": True,
        "Pactive_probe_not_spurion_parent_derived": False,
        "counterterm_forbidden_if_Pactive_probe_only": True,
        "counterterm_allowed_if_Pactive_physical_spurion": True,
        "epsilon_H_conditional_exact_readout": 1.0,
        "epsilon_H_parent_derived_unconditionally": False,
        "promotion_allowed": False,
        "next_target": "derive_Pactive_as_boundary_observable_not_action_spurion_or_freeze_epsilonH_as_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Action-level exact-readout gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
