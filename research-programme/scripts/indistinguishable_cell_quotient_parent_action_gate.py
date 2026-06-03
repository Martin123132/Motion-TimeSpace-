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
RUN_SLUG = "indistinguishable-cell-quotient-parent-action-gate"
STATUS = "indistinguishable_cell_quotient_template_constructed_parent_variable_origin_open"
CLAIM_CEILING = "quotient_parent_action_gate_no_unconditional_epsilonH_Bmem_or_parent_action_promotion"
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


def active_average(state: np.ndarray) -> float:
    return float(np.dot(active_mask(), state) / RANK_ACTIVE)


def trace_average(state: np.ndarray) -> float:
    return float(np.mean(state))


def q_trace_from_state(state: np.ndarray) -> float:
    return float(np.dot(active_mask(), state) / DIM_CELL)


def sorted_orbit_rep(state: np.ndarray) -> np.ndarray:
    return np.sort(state)


def invariants(state: np.ndarray) -> tuple[float, float, float]:
    return (float(np.sum(state)), float(np.sum(state**2)), float(np.sum(state**3)))


def parent_class_action(state: np.ndarray) -> float:
    return float(0.5 * np.sum((state - 1.0) ** 2))


def active_spurion_action(state: np.ndarray, marker: np.ndarray | None = None) -> float:
    if marker is None:
        marker = active_mask()
    return float(parent_class_action(state) - J_TEST * np.dot(marker, state))


def swap_active_inactive(state: np.ndarray) -> np.ndarray:
    swapped = state.copy()
    swapped[[0, 2]] = swapped[[2, 0]]
    return swapped


def rotate_sample_state() -> np.ndarray:
    state = np.ones(DIM_CELL)
    state[0] += J_TEST
    state[1] += 0.5 * J_TEST
    state[2] -= 0.25 * J_TEST
    return state


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "337-exact-parent-pullback-selection-rule-gate.md", "exact parent pullback theorem"),
        (ROOT / "339-Pactive-boundary-observable-Ward-gate.md", "Ward readout/material marker fork"),
        (ROOT / "340-full-cell-equivalence-gauge-redundancy-gate.md", "gauge redundancy versus global symmetry gate"),
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


def orbit_function_rows() -> list[dict[str, Any]]:
    state = rotate_sample_state()
    swapped = swap_active_inactive(state)
    marker = active_mask()
    swapped_marker = swap_active_inactive(marker)
    observables = [
        (
            "trace_average",
            trace_average(state),
            trace_average(swapped),
            "class_function_on_quotient",
            "bulk invariant readout",
        ),
        (
            "sorted_spectrum_first_three",
            tuple(np.round(sorted_orbit_rep(state)[:3], 12)),
            tuple(np.round(sorted_orbit_rep(swapped)[:3], 12)),
            "class_function_on_quotient",
            "basis-free orbit representative",
        ),
        (
            "power_sum_invariants",
            tuple(round(value, 12) for value in invariants(state)),
            tuple(round(value, 12) for value in invariants(swapped)),
            "class_function_on_quotient",
            "trace/power-sum parent data",
        ),
        (
            "fixed_active_average",
            active_average(state),
            active_average(swapped),
            "not_function_on_state_quotient",
            "depends on arbitrary labels",
        ),
        (
            "fixed_active_q_trace",
            q_trace_from_state(state),
            q_trace_from_state(swapped),
            "not_function_on_state_quotient",
            "same hazard as active amplitude readout",
        ),
        (
            "relational_active_average_with_transformed_marker",
            float(np.dot(marker, state) / np.sum(marker)),
            float(np.dot(swapped_marker, swapped) / np.sum(swapped_marker)),
            "function_on_extended_pair_quotient",
            "safe only if marker is observer/source dressing, not material",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for name, value, swapped_value, quotient_status, meaning in observables:
        rows.append(
            {
                "observable": name,
                "value": value,
                "value_after_active_inactive_swap": swapped_value,
                "orbit_constant": value == swapped_value,
                "quotient_status": quotient_status,
                "meaning": meaning,
            }
        )
    return rows


def quotient_action_rows() -> list[dict[str, Any]]:
    state = rotate_sample_state()
    swapped = swap_active_inactive(state)
    marker = active_mask()
    swapped_marker = swap_active_inactive(marker)
    cases = [
        {
            "case": "class_action_on_quotient",
            "state_space": "S27 orbits / sorted spectrum",
            "action_state": parent_class_action(state),
            "action_swapped": parent_class_action(swapped),
            "marker_role": "none",
            "meaning": "action descends to quotient and cannot distinguish active labels",
        },
        {
            "case": "symmetric_labelled_species_action",
            "state_space": "labelled vector with global S27 symmetry",
            "action_state": parent_class_action(state),
            "action_swapped": parent_class_action(swapped),
            "marker_role": "none",
            "meaning": "same formula as quotient case, but interpretation still allows physical species labels",
        },
        {
            "case": "fixed_active_spurion_action",
            "state_space": "labelled vector plus fixed active background",
            "action_state": active_spurion_action(state),
            "action_swapped": active_spurion_action(swapped),
            "marker_role": "fixed external P_active",
            "meaning": "breaks the quotient and shifts the active sector",
        },
        {
            "case": "covariant_material_marker_action",
            "state_space": "quotient of pair (state, marker)",
            "action_state": active_spurion_action(state, marker),
            "action_swapped": active_spurion_action(swapped, swapped_marker),
            "marker_role": "physical transforming marker",
            "meaning": "formally descends to extended quotient but reintroduces active physical data",
        },
    ]
    rows: list[dict[str, Any]] = []
    for case in cases:
        rows.append(
            {
                "case": case["case"],
                "state_space": case["state_space"],
                "action_state": case["action_state"],
                "action_swapped": case["action_swapped"],
                "descends_to_stated_space": abs(case["action_state"] - case["action_swapped"]) < 1.0e-12,
                "marker_role": case["marker_role"],
                "meaning": case["meaning"],
            }
        )
    return rows


def parent_variable_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "component_species_route",
            "parent_variable": "27 labelled fields h_i",
            "configuration_space": "R^27",
            "allowed_observables": "labelled observables become physical once a sector is selected",
            "quotient_derived": False,
            "counterterm_status": "allowed after active selection",
            "epsilon_status": "closure_or_fitted",
        },
        {
            "route": "quotient_orbit_route",
            "parent_variable": "orbit [h] under S27 or sorted spectrum/multiset",
            "configuration_space": "R^27/S27",
            "allowed_observables": "class functions only; active readout must be external/source/relational",
            "quotient_derived": "if parent is formulated directly on orbit space",
            "counterterm_status": "forbidden in bulk action",
            "epsilon_status": "conditional_theorem",
        },
        {
            "route": "basis_fibre_route",
            "parent_variable": "basis-free operator/current on finite internal fibre",
            "configuration_space": "operators modulo basis relabeling/conjugation",
            "allowed_observables": "trace/spectral data plus relational source insertions",
            "quotient_derived": "if cells are basis choices, not species",
            "counterterm_status": "forbidden unless marker field is added",
            "epsilon_status": "conditional_theorem",
        },
        {
            "route": "material_marker_route",
            "parent_variable": "state plus active marker/background m_i",
            "configuration_space": "(state, marker)/S27",
            "allowed_observables": "marker-local observables and marker-local action terms",
            "quotient_derived": "extended quotient only",
            "counterterm_status": "allowed",
            "epsilon_status": "closure_or_fitted",
        },
    ]


def quotient_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "Q1_parent_variables_are_unlabelled_orbits",
            "required_statement": "the basic 27-cell parent variable is an orbit/multiset/basis-free fibre object, not a labelled 27-tuple of species",
            "effect_if_true": "turns cell relabeling into gauge by construction",
            "current_status": "not_yet_parent_derived",
        },
        {
            "condition": "Q2_action_is_class_function",
            "required_statement": "the parent action depends only on trace/spectrum/orbit data",
            "effect_if_true": "bulk dynamics descends to R^27/S27",
            "current_status": "conditional_template_verified",
        },
        {
            "condition": "Q3_observables_are_class_functions_or_sources_at_zero",
            "required_statement": "physical bulk observables are orbit-constant; non-invariant readouts appear only as zero-source insertions",
            "effect_if_true": "forbids fixed P_active as physical observable or action term",
            "current_status": "conditional_template_verified",
        },
        {
            "condition": "Q4_no_marker_extension",
            "required_statement": "the parent configuration space is not enlarged to include an active marker/background field",
            "effect_if_true": "blocks covariant material-spurion counterterms",
            "current_status": "open",
        },
        {
            "condition": "Q5_relational_readout_has_no_backreaction",
            "required_statement": "observer/source reference data used for active readout is external and evaluated at zero source",
            "effect_if_true": "keeps readout measurable without changing parent dynamics",
            "current_status": "open",
        },
        {
            "condition": "Q6_effective_action_remains_class_function",
            "required_statement": "coarse-grained/effective action is generated on quotient space, not labelled space after gauge choice",
            "effect_if_true": "prevents residual EFT counterterms from returning",
            "current_status": "open",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma": "same_formula_different_state_space",
            "statement": "The same symmetric action formula can live on labelled configuration space or quotient configuration space.",
            "consequence": "the formula alone does not derive gauge redundancy; the parent variable/state-space definition must do it.",
        },
        {
            "lemma": "non_class_readout_not_quotient_observable",
            "statement": "Fixed active readout is not constant on S27 orbits for nonuniform states.",
            "consequence": "P_active cannot be a physical bulk observable on the state quotient.",
        },
        {
            "lemma": "extended_quotient_marker_no_go",
            "statement": "A material marker can make active couplings invariant on an extended quotient of (state, marker).",
            "consequence": "quotienting alone is insufficient unless the parent forbids marker variables.",
        },
        {
            "lemma": "effective_labelled_EFT_no_go",
            "statement": "If the quotient is gauge-fixed and then treated as labelled EFT data, residual active counterterms return.",
            "consequence": "effective corrections must be generated as class functions on quotient space.",
        },
    ]


def gate_rows(
    sources: list[dict[str, Any]],
    orbit_rows: list[dict[str, Any]],
    action_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    by_observable = {row["observable"]: row for row in orbit_rows}
    by_action = {row["case"]: row for row in action_rows}
    return [
        {"gate": "source_paths_exist", "status": "pass" if sources_ok else "fail", "evidence": sources_ok},
        {
            "gate": "trace_and_spectrum_are_orbit_functions",
            "status": "pass"
            if bool(by_observable["trace_average"]["orbit_constant"])
            and bool(by_observable["sorted_spectrum_first_three"]["orbit_constant"])
            and bool(by_observable["power_sum_invariants"]["orbit_constant"])
            else "fail",
            "evidence": "trace/spectrum/power sums unchanged under active-inactive swap",
        },
        {
            "gate": "fixed_active_readout_is_not_quotient_function",
            "status": "pass" if not bool(by_observable["fixed_active_average"]["orbit_constant"]) else "fail",
            "evidence": f"{by_observable['fixed_active_average']['value']} -> {by_observable['fixed_active_average']['value_after_active_inactive_swap']}",
        },
        {
            "gate": "relational_readout_is_extended_quotient_function",
            "status": "pass"
            if bool(by_observable["relational_active_average_with_transformed_marker"]["orbit_constant"])
            else "fail",
            "evidence": by_observable["relational_active_average_with_transformed_marker"]["value"],
        },
        {
            "gate": "class_action_descends_to_quotient",
            "status": "pass" if bool(by_action["class_action_on_quotient"]["descends_to_stated_space"]) else "fail",
            "evidence": by_action["class_action_on_quotient"]["action_state"],
        },
        {
            "gate": "same_symmetric_formula_does_not_select_quotient_over_species",
            "status": "fail",
            "evidence": "class action and labelled-species action have identical invariant formula but different physical state spaces",
        },
        {
            "gate": "fixed_active_spurion_breaks_state_quotient",
            "status": "pass" if not bool(by_action["fixed_active_spurion_action"]["descends_to_stated_space"]) else "fail",
            "evidence": f"{by_action['fixed_active_spurion_action']['action_state']} vs {by_action['fixed_active_spurion_action']['action_swapped']}",
        },
        {
            "gate": "covariant_material_marker_descends_to_extended_quotient",
            "status": "pass" if bool(by_action["covariant_material_marker_action"]["descends_to_stated_space"]) else "fail",
            "evidence": "extended quotient exists but includes physical active marker",
        },
        {
            "gate": "parent_variables_prove_unlabelled_orbit_space",
            "status": "fail",
            "evidence": "current corpus has a route/contract but not a parent variable derivation",
        },
        {
            "gate": "parent_theory_proves_no_marker_extension",
            "status": "fail",
            "evidence": "no parent statement forbids marker/background variables",
        },
        {
            "gate": "effective_action_proven_class_function",
            "status": "fail",
            "evidence": "no effective quotient construction or Ward identity is supplied",
        },
        {
            "gate": "epsilon_H_parent_derived_unconditionally",
            "status": "fail",
            "evidence": "requires Q1-Q6",
        },
        {
            "gate": "Bmem_parent_promotion_allowed",
            "status": "fail",
            "evidence": "quotient origin, no-marker, Hstar=H0, and correction stability remain open",
        },
        {
            "gate": "quotient_parent_action_contract_available",
            "status": "pass",
            "evidence": "Q1-Q6 written as exact parent-variable contract",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The indistinguishable-cell route is viable only if the parent variable is an unlabelled orbit/multiset or "
                "basis-free finite-fibre object and the action/observables are class functions on R^27/S27. This would make "
                "fixed P_active nonphysical in the bulk and keep active readout as source/relational data. But the current "
                "corpus has not yet derived that variable choice; the same symmetric formula can still describe physical "
                "species, and a material-marker extension reopens active counterterms."
            ),
            "next_target": "derive_parent_finite_fibre_basis_relabeling_or_freeze_epsilonH_as_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    orbit = orbit_function_rows()
    actions = quotient_action_rows()
    routes = parent_variable_route_rows()
    contract = quotient_contract_rows()
    no_gos = no_go_rows()
    gates = gate_rows(sources, orbit, actions)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": (sources, ["source", "role", "exists", "issue"]),
        "orbit_function_tests.csv": (
            orbit,
            [
                "observable",
                "value",
                "value_after_active_inactive_swap",
                "orbit_constant",
                "quotient_status",
                "meaning",
            ],
        ),
        "quotient_action_tests.csv": (
            actions,
            ["case", "state_space", "action_state", "action_swapped", "descends_to_stated_space", "marker_role", "meaning"],
        ),
        "parent_variable_route_audit.csv": (
            routes,
            [
                "route",
                "parent_variable",
                "configuration_space",
                "allowed_observables",
                "quotient_derived",
                "counterterm_status",
                "epsilon_status",
            ],
        ),
        "quotient_parent_action_contract.csv": (
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
        "quotient_parent_action_template": True,
        "class_action_descends_to_quotient": True,
        "fixed_Pactive_not_quotient_observable": True,
        "parent_variables_prove_unlabelled_orbit_space": False,
        "material_marker_extension_hazard_open": True,
        "effective_action_class_function_derived": False,
        "epsilon_H_parent_derived_unconditionally": False,
        "promotion_allowed": False,
        "next_target": "derive_parent_finite_fibre_basis_relabeling_or_freeze_epsilonH_as_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Indistinguishable-cell quotient parent-action gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
