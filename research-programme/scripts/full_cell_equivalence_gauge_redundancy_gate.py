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
RUN_SLUG = "full-cell-equivalence-gauge-redundancy-gate"
STATUS = "full_cell_equivalence_gauge_route_sharpened_but_not_parent_derived"
CLAIM_CEILING = "gauge_redundancy_gate_no_unconditional_epsilonH_Bmem_or_parent_action_promotion"
DIM_CELL = 27
RANK_ACTIVE = 2
Q_TRACE = Fraction(RANK_ACTIVE, DIM_CELL)
J_TEST = 0.0061980866083466


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


def active_inactive_swap_perm() -> np.ndarray:
    perm = np.arange(DIM_CELL)
    perm[[0, 2]] = perm[[2, 0]]
    return perm


def cycle_perm() -> np.ndarray:
    return np.roll(np.arange(DIM_CELL), -1)


def apply_perm(vector: np.ndarray, perm: np.ndarray) -> np.ndarray:
    return vector[perm]


def fixed_active_average(state: np.ndarray) -> float:
    return float(np.dot(active_mask(), state) / RANK_ACTIVE)


def full_average(state: np.ndarray) -> float:
    return float(np.mean(state))


def q_trace_from_readout(state: np.ndarray) -> float:
    return float(np.dot(active_mask(), state) / DIM_CELL)


def relational_active_average(state: np.ndarray, reference_mask: np.ndarray) -> float:
    return float(np.dot(reference_mask, state) / np.sum(reference_mask))


def parent_action(state: np.ndarray) -> float:
    return float(0.5 * np.sum((state - 1.0) ** 2))


def physical_marker_action(state: np.ndarray) -> float:
    return float(parent_action(state) - J_TEST * np.dot(active_mask(), state))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "337-exact-parent-pullback-selection-rule-gate.md", "conditional exact-pullback theorem"),
        (ROOT / "338-action-level-exact-readout-gate.md", "action-level source/spurion split"),
        (ROOT / "339-Pactive-boundary-observable-Ward-gate.md", "Ward route and material-spurion hazard"),
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


def state_witness_rows() -> list[dict[str, Any]]:
    uniform = np.ones(DIM_CELL)
    nonuniform = np.ones(DIM_CELL)
    nonuniform[:RANK_ACTIVE] += J_TEST
    swap = active_inactive_swap_perm()
    cyclic = cycle_perm()
    witnesses = [
        ("uniform_parent_solution", uniform),
        ("active_perturbed_state", nonuniform),
    ]
    rows: list[dict[str, Any]] = []
    for name, state in witnesses:
        swapped = apply_perm(state, swap)
        cycled = apply_perm(state, cyclic)
        reference = active_mask()
        swapped_reference = apply_perm(reference, swap)
        rows.append(
            {
                "state": name,
                "parent_action": parent_action(state),
                "parent_action_after_active_inactive_swap": parent_action(swapped),
                "parent_action_invariant": abs(parent_action(state) - parent_action(swapped)) < 1.0e-12,
                "fixed_active_average": fixed_active_average(state),
                "fixed_active_average_after_swap": fixed_active_average(swapped),
                "fixed_active_readout_gauge_invariant": abs(fixed_active_average(state) - fixed_active_average(swapped)) < 1.0e-12,
                "orbit_average_readout": full_average(state),
                "orbit_average_after_cycle": full_average(cycled),
                "relational_readout_with_transformed_reference": relational_active_average(swapped, swapped_reference),
                "relational_readout_invariant": abs(
                    relational_active_average(state, reference) - relational_active_average(swapped, swapped_reference)
                )
                < 1.0e-12,
            }
        )
    return rows


def label_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "interpretation": "gauge_label_redundancy",
            "cell_labels_meaning": "arbitrary enumeration of indistinguishable parent channels",
            "state_space": "orbits under S27",
            "allowed_bulk_terms": "S27-invariant parent pullbacks only",
            "Pactive_status": "not a bulk field; source-at-zero or relational readout only",
            "counterterm_status": "forbidden if no material marker exists",
            "epsilon_status": "conditional theorem",
        },
        {
            "interpretation": "global_symmetry_physical_species",
            "cell_labels_meaning": "physically distinct but symmetric species/sectors",
            "state_space": "labelled configurations",
            "allowed_bulk_terms": "symmetric action plus possible physical symmetry breaking",
            "Pactive_status": "can become an explicit spurion/defect",
            "counterterm_status": "allowed once active sector is physically selected",
            "epsilon_status": "closure or fitted",
        },
        {
            "interpretation": "gauge_fixed_representative",
            "cell_labels_meaning": "chosen representative of a gauge orbit",
            "state_space": "one representative plus gauge-fixing conditions",
            "allowed_bulk_terms": "must descend from gauge-invariant parent terms",
            "Pactive_status": "gauge choice, not physical tensor",
            "counterterm_status": "forbidden only if gauge fixing is not treated as new EFT data",
            "epsilon_status": "conditional theorem",
        },
        {
            "interpretation": "relational_boundary_reference",
            "cell_labels_meaning": "active cells defined relative to an external observer/source frame",
            "state_space": "gauge orbits with relationally dressed observable",
            "allowed_bulk_terms": "parent-invariant bulk; source insertion evaluated at zero",
            "Pactive_status": "observable dressing",
            "counterterm_status": "forbidden if reference has no variational backreaction",
            "epsilon_status": "conditional theorem",
        },
        {
            "interpretation": "material_marker_or_boundary_defect",
            "cell_labels_meaning": "active rank-2 mark is a real physical structure",
            "state_space": "parent fields plus marker field/background",
            "allowed_bulk_terms": "gauge-covariant terms built from marker",
            "Pactive_status": "physical spurion",
            "counterterm_status": "allowed",
            "epsilon_status": "closure or fitted",
        },
    ]


def action_invariance_rows() -> list[dict[str, Any]]:
    state = np.ones(DIM_CELL)
    state[:RANK_ACTIVE] += J_TEST
    swap = active_inactive_swap_perm()
    swapped_state = apply_perm(state, swap)
    marker = active_mask()
    swapped_marker = apply_perm(marker, swap)
    parent_delta = parent_action(state) - parent_action(swapped_state)
    fixed_marker_delta = physical_marker_action(state) - physical_marker_action(swapped_state)
    covariant_marker_delta = (
        parent_action(state)
        - J_TEST * np.dot(marker, state)
        - (parent_action(swapped_state) - J_TEST * np.dot(swapped_marker, swapped_state))
    )
    return [
        {
            "action_case": "parent_label_symmetric_action",
            "delta_under_active_inactive_swap": parent_delta,
            "invariant": abs(parent_delta) < 1.0e-12,
            "meaning": "the finite witness action is label-symmetric",
        },
        {
            "action_case": "fixed_Pactive_physical_action",
            "delta_under_active_inactive_swap": fixed_marker_delta,
            "invariant": abs(fixed_marker_delta) < 1.0e-12,
            "meaning": "a fixed physical active marker breaks full cell equivalence",
        },
        {
            "action_case": "transforming_marker_covariant_action",
            "delta_under_active_inactive_swap": covariant_marker_delta,
            "invariant": abs(covariant_marker_delta) < 1.0e-12,
            "meaning": "a transforming material marker can be formally invariant while reopening counterterms",
        },
    ]


def gauge_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "G1_indistinguishable_parent_cells",
            "required_statement": "the 27 cell labels are arbitrary enumeration labels of one parent structure, not physical species",
            "effect_if_true": "turns S27 from global symmetry into redundancy of description",
            "current_status": "not_yet_parent_derived",
        },
        {
            "condition": "G2_physical_state_space_is_quotient",
            "required_statement": "physical states are S27 orbits and not labelled configurations",
            "effect_if_true": "non-invariant fixed-active readouts are not physical bulk observables",
            "current_status": "not_yet_parent_derived",
        },
        {
            "condition": "G3_bulk_action_descends_to_quotient",
            "required_statement": "every physical bulk term is S27-invariant before gauge fixing/readout",
            "effect_if_true": "forbids lambda_mem P_active in bulk dynamics",
            "current_status": "conditional_from_Ward_route",
        },
        {
            "condition": "G4_gauge_fixing_not_new_EFT_stage",
            "required_statement": "choosing an active representative does not license all residual-invariant counterterms",
            "effect_if_true": "prevents post-gauge-fix lambda_mem P_active",
            "current_status": "open",
        },
        {
            "condition": "G5_relational_readout_not_material_marker",
            "required_statement": "active readout is dressed to an observer/source frame with no physical marker action",
            "effect_if_true": "allows active measurement without active bulk spurion",
            "current_status": "open",
        },
        {
            "condition": "G6_effective_action_respects_parent_quotient",
            "required_statement": "coarse-grained/effective corrections are functions on quotient space, not labelled-space EFT terms",
            "effect_if_true": "protects the amplitude beyond the tree-level witness",
            "current_status": "open",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma": "symmetry_not_gauge_no_go",
            "statement": "An invariant action alone does not prove that label-related states are the same physical state.",
            "consequence": "full cell equivalence must be promoted to quotient/gauge structure, not merely used as symmetry.",
        },
        {
            "lemma": "fixed_readout_not_gauge_invariant",
            "statement": "For nonuniform states, a fixed active-cell readout changes under an active/inactive permutation.",
            "consequence": "P_active needs relational dressing or source-at-zero status if labels are gauge.",
        },
        {
            "lemma": "relational_marker_fork",
            "statement": "A transformed reference mask makes the readout gauge-invariant, but a physical reference mask is a material marker.",
            "consequence": "the parent theory must distinguish observer dressing from action spurion.",
        },
        {
            "lemma": "gauge_fixing_EFT_hazard",
            "statement": "Writing an EFT after gauge fixing can reintroduce residual-invariant active counterterms.",
            "consequence": "effective corrections must descend from the parent quotient.",
        },
    ]


def gate_rows(
    sources: list[dict[str, Any]],
    witnesses: list[dict[str, Any]],
    actions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    by_state = {row["state"]: row for row in witnesses}
    by_action = {row["action_case"]: row for row in actions}
    uniform = by_state["uniform_parent_solution"]
    nonuniform = by_state["active_perturbed_state"]
    parent = by_action["parent_label_symmetric_action"]
    fixed = by_action["fixed_Pactive_physical_action"]
    covariant = by_action["transforming_marker_covariant_action"]
    return [
        {"gate": "source_paths_exist", "status": "pass" if sources_ok else "fail", "evidence": sources_ok},
        {
            "gate": "parent_witness_action_is_label_symmetric",
            "status": "pass" if bool(parent["invariant"]) else "fail",
            "evidence": parent["delta_under_active_inactive_swap"],
        },
        {
            "gate": "label_symmetry_alone_proves_gauge_redundancy",
            "status": "fail",
            "evidence": "an invariant action may describe global symmetry among physical species unless state space is quotiented",
        },
        {
            "gate": "uniform_parent_solution_readout_is_safe",
            "status": "pass" if abs(float(uniform["fixed_active_average"]) - 1.0) < 1.0e-12 else "fail",
            "evidence": uniform["fixed_active_average"],
        },
        {
            "gate": "fixed_active_readout_not_gauge_invariant_for_nonuniform_states",
            "status": "pass" if not bool(nonuniform["fixed_active_readout_gauge_invariant"]) else "fail",
            "evidence": f"{nonuniform['fixed_active_average']} -> {nonuniform['fixed_active_average_after_swap']}",
        },
        {
            "gate": "relational_reference_readout_is_invariant",
            "status": "pass" if bool(nonuniform["relational_readout_invariant"]) else "fail",
            "evidence": nonuniform["relational_readout_with_transformed_reference"],
        },
        {
            "gate": "fixed_Pactive_action_breaks_full_cell_equivalence",
            "status": "pass" if not bool(fixed["invariant"]) else "fail",
            "evidence": fixed["delta_under_active_inactive_swap"],
        },
        {
            "gate": "transforming_marker_keeps_formal_invariance",
            "status": "pass" if bool(covariant["invariant"]) else "fail",
            "evidence": covariant["delta_under_active_inactive_swap"],
        },
        {
            "gate": "parent_theory_proves_no_material_marker",
            "status": "fail",
            "evidence": "current route has no parent statement forbidding transforming marker fields or physical boundary defects",
        },
        {
            "gate": "physical_state_space_quotient_parent_derived",
            "status": "fail",
            "evidence": "current route has a quotient contract, not a derivation from a parent action",
        },
        {
            "gate": "effective_corrections_descend_to_quotient",
            "status": "fail",
            "evidence": "no correction-level quotient/Ward identity has been supplied",
        },
        {
            "gate": "epsilon_H_parent_derived_unconditionally",
            "status": "fail",
            "evidence": "requires G1-G6",
        },
        {
            "gate": "Bmem_parent_promotion_allowed",
            "status": "fail",
            "evidence": "gauge redundancy, no-marker, Hstar=H0, and correction stability remain open",
        },
        {
            "gate": "gauge_redundancy_contract_available",
            "status": "pass",
            "evidence": "G1-G6 written as the next parent-action contract",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The gauge route has been sharpened: if the 27 cells are arbitrary labels and physical states are S27 orbits, "
                "then fixed P_active is not a bulk observable and lambda_mem P_active is forbidden. Active readout must be "
                "source-at-zero or relationally dressed. However, action invariance alone does not prove gauge redundancy; "
                "a global symmetry among physical species or a transforming material marker still reopens the counterterm."
            ),
            "next_target": "derive_indistinguishable_cell_quotient_from_parent_action_or_freeze_epsilonH_as_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    witnesses = state_witness_rows()
    label_status = label_status_rows()
    actions = action_invariance_rows()
    contract = gauge_contract_rows()
    no_gos = no_go_rows()
    gates = gate_rows(sources, witnesses, actions)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": (sources, ["source", "role", "exists", "issue"]),
        "state_orbit_witnesses.csv": (
            witnesses,
            [
                "state",
                "parent_action",
                "parent_action_after_active_inactive_swap",
                "parent_action_invariant",
                "fixed_active_average",
                "fixed_active_average_after_swap",
                "fixed_active_readout_gauge_invariant",
                "orbit_average_readout",
                "orbit_average_after_cycle",
                "relational_readout_with_transformed_reference",
                "relational_readout_invariant",
            ],
        ),
        "label_interpretation_audit.csv": (
            label_status,
            [
                "interpretation",
                "cell_labels_meaning",
                "state_space",
                "allowed_bulk_terms",
                "Pactive_status",
                "counterterm_status",
                "epsilon_status",
            ],
        ),
        "action_invariance_tests.csv": (
            actions,
            ["action_case", "delta_under_active_inactive_swap", "invariant", "meaning"],
        ),
        "gauge_redundancy_contract.csv": (
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
        "parent_action_label_symmetric": True,
        "label_symmetry_alone_derives_gauge": False,
        "quotient_state_space_contract": True,
        "physical_state_space_quotient_parent_derived": False,
        "relational_readout_route_available": True,
        "material_marker_hazard_open": True,
        "epsilon_H_parent_derived_unconditionally": False,
        "promotion_allowed": False,
        "next_target": "derive_indistinguishable_cell_quotient_from_parent_action_or_freeze_epsilonH_as_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Full-cell-equivalence gauge-redundancy gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
