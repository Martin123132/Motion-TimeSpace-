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
RUN_SLUG = "Pactive-boundary-observable-Ward-gate"
STATUS = "Pactive_probe_route_conditionally_supported_gauge_redundancy_and_no_material_defect_open"
CLAIM_CEILING = "Ward_readout_gate_no_unconditional_epsilonH_Bmem_or_parent_action_promotion"
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


def orbit_average_mask() -> np.ndarray:
    return np.full(DIM_CELL, RANK_ACTIVE / DIM_CELL, dtype=float)


def swap_matrix(i: int, j: int) -> np.ndarray:
    matrix = np.eye(DIM_CELL)
    matrix[[i, j], :] = matrix[[j, i], :]
    return matrix


def active_inactive_swap() -> np.ndarray:
    return swap_matrix(0, 2)


def ward_norm(mask: np.ndarray, source_strength: float = 1.0) -> float:
    generator = active_inactive_swap()
    return float(abs(source_strength) * np.linalg.norm(mask - generator.T @ mask))


def active_average(weights: np.ndarray) -> float:
    mask = active_mask()
    return float(np.dot(mask, weights) / RANK_ACTIVE)


def q_trace(weights: np.ndarray) -> float:
    return float(np.dot(active_mask(), weights) / DIM_CELL)


def full_average(weights: np.ndarray) -> float:
    return float(np.mean(weights))


def trace_normalized(weights: np.ndarray) -> np.ndarray:
    average = full_average(weights)
    if abs(average) < 1.0e-14:
        raise ValueError("Cannot trace-normalize zero-average weights.")
    return weights / average


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "336-no-later-active-counterterm-theorem-gate.md", "no-later active counterterm route"),
        (ROOT / "337-exact-parent-pullback-selection-rule-gate.md", "exact parent pullback theorem"),
        (ROOT / "338-action-level-exact-readout-gate.md", "action-level readout versus spurion gate"),
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


def ward_identity_rows() -> list[dict[str, Any]]:
    active = active_mask()
    averaged = orbit_average_mask()
    return [
        {
            "term": "physical_fixed_Pactive_bulk_term",
            "source_strength": J_TEST,
            "mask_type": "fixed_active_mask",
            "Ward_norm_under_active_inactive_swap": ward_norm(active, J_TEST),
            "Ward_status": "violates_full_cell_gauge_redundancy",
            "meaning": "a nonzero physical fixed-P_active coupling is not allowed if full cell equivalence is gauge",
        },
        {
            "term": "source_at_zero_Pactive_probe",
            "source_strength": 0.0,
            "mask_type": "fixed_active_mask",
            "Ward_norm_under_active_inactive_swap": ward_norm(active, 0.0),
            "Ward_status": "physical_action_identity_restored",
            "meaning": "P_active may be used as a source insertion only after variation and evaluated at J=0",
        },
        {
            "term": "orbit_averaged_bulk_completion",
            "source_strength": J_TEST,
            "mask_type": "orbit_average_rank2_mask",
            "Ward_norm_under_active_inactive_swap": ward_norm(averaged, J_TEST),
            "Ward_status": "gauge_invariant_but_not_active_specific",
            "meaning": "the gauge-invariant completion is uniform over cells and cannot carry active contrast",
        },
        {
            "term": "transforming_material_spurion",
            "source_strength": J_TEST,
            "mask_type": "m_i transforms with gauge action",
            "Ward_norm_under_active_inactive_swap": 0.0,
            "Ward_status": "formally_invariant_but_physical_defect",
            "meaning": "if a real material marker transforms and then is fixed to P_active, the active counterterm is physical",
        },
    ]


def orbit_completion_rows() -> list[dict[str, Any]]:
    active = active_mask()
    averaged = orbit_average_mask()
    fixed_weights = np.ones(DIM_CELL) + J_TEST * active
    uniform_weights = np.ones(DIM_CELL) + J_TEST * averaged
    norm_fixed = trace_normalized(fixed_weights)
    norm_uniform = trace_normalized(uniform_weights)
    return [
        {
            "completion": "fixed_Pactive_physical_term",
            "mask_average": "two selected cells have weight 1, others 0",
            "full_trace_average_before_normalization": full_average(fixed_weights),
            "epsilon_H_after_trace_normalization": active_average(norm_fixed),
            "q_trace_after_trace_normalization": q_trace(norm_fixed),
            "active_contrast_survives": True,
            "meaning": "this shifts the active block and reopens epsilon_H",
        },
        {
            "completion": "S27_orbit_average_of_Pactive",
            "mask_average": f"every cell has weight {Q_TRACE.numerator}/{Q_TRACE.denominator}",
            "full_trace_average_before_normalization": full_average(uniform_weights),
            "epsilon_H_after_trace_normalization": active_average(norm_uniform),
            "q_trace_after_trace_normalization": q_trace(norm_uniform),
            "active_contrast_survives": False,
            "meaning": "the gauge-invariant completion preserves epsilon_H=1 but removes active-specific coupling",
        },
    ]


def boundary_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "W1_full_cell_equivalence_is_gauge_redundancy",
            "required_statement": "cell labels are gauge copies before readout, not distinct physical species",
            "effect_if_true": "non-invariant fixed P_active terms are forbidden in the bulk action",
            "current_status": "not_yet_parent_derived",
        },
        {
            "condition": "W2_Pactive_enters_only_as_external_source",
            "required_statement": "P_active couples to a source used for differentiating observables, with physical limit J=0",
            "effect_if_true": "readout can be computed without shifting the parent solution",
            "current_status": "conditional_contract",
        },
        {
            "condition": "W3_no_material_marker_field",
            "required_statement": "there is no dynamical or fixed material field m_i whose background value is P_active",
            "effect_if_true": "prevents spurion logic from making active counterterms gauge-covariant",
            "current_status": "open",
        },
        {
            "condition": "W4_boundary_readout_has_no_variational_backreaction",
            "required_statement": "boundary/readout insertion either is evaluated at zero source or has Dirichlet data that does not alter bulk equations",
            "effect_if_true": "protects local dynamics and amplitude from the measurement mark",
            "current_status": "open",
        },
        {
            "condition": "W5_effective_corrections_satisfy_parent_Ward_identity",
            "required_statement": "coarse-graining/loops respect the full-cell Ward identity rather than only residual symmetry",
            "effect_if_true": "forbids lambda_mem P_active from returning as a generated counterterm",
            "current_status": "open",
        },
        {
            "condition": "W6_observable_is_relationally_dressed",
            "required_statement": "the active readout is defined relative to a boundary/observer frame, not as a bulk gauge-breaking observable",
            "effect_if_true": "makes P_active measurable without putting it into the physical action",
            "current_status": "open",
        },
    ]


def spurion_hazard_rows() -> list[dict[str, Any]]:
    return [
        {
            "hazard": "fixed_external_bulk_spurion",
            "description": "P_active is placed in the physical bulk action as a fixed background tensor",
            "Ward_status": "violates full gauge redundancy",
            "amplitude_status": "not allowed if W1 is true; otherwise epsilon_H is free",
        },
        {
            "hazard": "transforming_material_spurion",
            "description": "a marker field m_i transforms under cell permutations and is then set to P_active",
            "Ward_status": "formally invariant",
            "amplitude_status": "counterterms allowed because the active mark is physical",
        },
        {
            "hazard": "boundary_defect",
            "description": "the active rank-2 mark is a real boundary/defect with action terms",
            "Ward_status": "allowed only with boundary Ward accounting",
            "amplitude_status": "free boundary coefficients unless fixed by an extra boundary principle",
        },
        {
            "hazard": "residual_EFT_after_gauge_fixing",
            "description": "one gauge-fixes to an active/inactive split and then writes all residual invariants",
            "Ward_status": "misses parent Ward identity",
            "amplitude_status": "lambda_mem P_active returns",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma": "Ward_forbidden_fixed_projector",
            "statement": "If full cell equivalence is gauge, a fixed non-invariant P_active cannot appear in the physical bulk action.",
            "consequence": "this supports P_active as source/readout only, not as an action spurion.",
        },
        {
            "lemma": "orbit_average_erases_active_contrast",
            "statement": "The full-gauge orbit average of a rank-2 active mask is the uniform mask 2/27 on every cell.",
            "consequence": "the gauge-invariant bulk completion does not generate an active-block amplitude shift.",
        },
        {
            "lemma": "material_spurion_escape",
            "statement": "A transforming marker field can make P_active-like terms formally invariant.",
            "consequence": "the parent theory must forbid a physical marker/defect if epsilon_H is to be derived.",
        },
        {
            "lemma": "source_zero_safety",
            "statement": "A source insertion used only at J=0 can define a readout without modifying physical equations.",
            "consequence": "observable readout is safe only if the source is not promoted to a physical coupling.",
        },
    ]


def gate_rows(sources: list[dict[str, Any]], ward_rows: list[dict[str, Any]], orbit_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    by_term = {row["term"]: row for row in ward_rows}
    by_completion = {row["completion"]: row for row in orbit_rows}
    fixed = by_term["physical_fixed_Pactive_bulk_term"]
    source_zero = by_term["source_at_zero_Pactive_probe"]
    averaged = by_term["orbit_averaged_bulk_completion"]
    material = by_term["transforming_material_spurion"]
    fixed_completion = by_completion["fixed_Pactive_physical_term"]
    average_completion = by_completion["S27_orbit_average_of_Pactive"]
    return [
        {"gate": "source_paths_exist", "status": "pass" if sources_ok else "fail", "evidence": sources_ok},
        {
            "gate": "fixed_Pactive_bulk_term_violates_parent_Ward",
            "status": "pass" if float(fixed["Ward_norm_under_active_inactive_swap"]) > 1.0e-12 else "fail",
            "evidence": fixed["Ward_norm_under_active_inactive_swap"],
        },
        {
            "gate": "source_at_zero_restores_physical_Ward_identity",
            "status": "pass" if float(source_zero["Ward_norm_under_active_inactive_swap"]) < 1.0e-12 else "fail",
            "evidence": source_zero["Ward_norm_under_active_inactive_swap"],
        },
        {
            "gate": "orbit_average_is_parent_Ward_invariant",
            "status": "pass" if float(averaged["Ward_norm_under_active_inactive_swap"]) < 1.0e-12 else "fail",
            "evidence": averaged["Ward_norm_under_active_inactive_swap"],
        },
        {
            "gate": "orbit_average_erases_active_amplitude_shift",
            "status": "pass"
            if abs(float(average_completion["epsilon_H_after_trace_normalization"]) - 1.0) < 1.0e-12
            else "fail",
            "evidence": average_completion["epsilon_H_after_trace_normalization"],
        },
        {
            "gate": "fixed_Pactive_spurion_shifts_active_amplitude",
            "status": "pass"
            if abs(float(fixed_completion["epsilon_H_after_trace_normalization"]) - 1.0) > 1.0e-6
            else "fail",
            "evidence": fixed_completion["epsilon_H_after_trace_normalization"],
        },
        {
            "gate": "transforming_material_spurion_reopens_counterterm",
            "status": "pass" if float(material["Ward_norm_under_active_inactive_swap"]) < 1.0e-12 else "fail",
            "evidence": "formally Ward-invariant if marker field transforms, so parent must forbid material marker",
        },
        {
            "gate": "parent_theory_proves_full_cell_equivalence_is_gauge",
            "status": "fail",
            "evidence": "current branch uses full cell equivalence as a selection principle but has not derived gauge redundancy",
        },
        {
            "gate": "parent_theory_proves_no_material_marker_or_boundary_defect",
            "status": "fail",
            "evidence": "no parent Ward/BRST/boundary identity yet forbids a physical active marker",
        },
        {
            "gate": "effective_corrections_obey_parent_Ward_identity",
            "status": "fail",
            "evidence": "no correction-level Ward identity has been supplied",
        },
        {
            "gate": "epsilon_H_parent_derived_unconditionally",
            "status": "fail",
            "evidence": "requires W1-W6, especially gauge redundancy and no material spurion",
        },
        {
            "gate": "Bmem_parent_promotion_allowed",
            "status": "fail",
            "evidence": "epsilon_H, Hstar=H0, and correction stability are not fully parent-owned",
        },
        {
            "gate": "Ward_readout_contract_available",
            "status": "pass",
            "evidence": "W1-W6 written as the next parent-action contract",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "A Ward-style route can support P_active as a readout: if full cell equivalence is a gauge redundancy, fixed "
                "P_active bulk terms violate the parent Ward identity, while source-at-zero insertions are safe and the only "
                "gauge-invariant bulk completion is the orbit-averaged uniform mask. But this is not yet an unconditional "
                "derivation because the parent theory has not proved full cell equivalence is gauge, nor ruled out a "
                "transforming material marker or boundary defect that would make active counterterms physical."
            ),
            "next_target": "derive_full_cell_equivalence_as_gauge_redundancy_or_freeze_epsilonH_as_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    ward = ward_identity_rows()
    orbit = orbit_completion_rows()
    contract = boundary_contract_rows()
    hazards = spurion_hazard_rows()
    no_gos = no_go_rows()
    gates = gate_rows(sources, ward, orbit)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": (sources, ["source", "role", "exists", "issue"]),
        "Ward_identity_tests.csv": (
            ward,
            ["term", "source_strength", "mask_type", "Ward_norm_under_active_inactive_swap", "Ward_status", "meaning"],
        ),
        "orbit_completion_tests.csv": (
            orbit,
            [
                "completion",
                "mask_average",
                "full_trace_average_before_normalization",
                "epsilon_H_after_trace_normalization",
                "q_trace_after_trace_normalization",
                "active_contrast_survives",
                "meaning",
            ],
        ),
        "boundary_readout_contract.csv": (
            contract,
            ["condition", "required_statement", "effect_if_true", "current_status"],
        ),
        "spurion_hazard_audit.csv": (
            hazards,
            ["hazard", "description", "Ward_status", "amplitude_status"],
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
        "Ward_readout_contract": True,
        "fixed_Pactive_bulk_forbidden_if_gauge": True,
        "source_at_zero_safe": True,
        "orbit_average_erases_active_contrast": True,
        "material_spurion_hazard_open": True,
        "full_cell_equivalence_gauge_derived": False,
        "Pactive_probe_not_spurion_parent_derived": False,
        "epsilon_H_parent_derived_unconditionally": False,
        "promotion_allowed": False,
        "next_target": "derive_full_cell_equivalence_as_gauge_redundancy_or_freeze_epsilonH_as_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="P_active boundary-observable Ward gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
