from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "domain-free-boundary-Euler-equation"
STATUS = "Ccoh_free_boundary_Euler_equation_derived_but_degenerate_domain_not_parent_selected"
CLAIM_CEILING = "domain_shape_derivative_derived_no_domain_selection_or_local_GR_promotion"


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


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "62-domain-field-chiD-action-contract.md", "domain selector action contract"),
        (ROOT / "64-binding-invariant-domain-selector-attempt.md", "C_coh invariant definition and arena split"),
        (ROOT / "68-chiD-gated-memory-conservation-contract.md", "Bianchi/conservation contract for gated memory"),
        (ROOT / "143-domain-selector-variational-action-attempt.md", "previous free-boundary gap"),
        (ROOT / "276-coherent-domain-projector-from-parent-variables.md", "fixed-D Qcoh projection and domain-selector blocker"),
        (ROOT / "scripts" / "domain_free_boundary_Euler_equation.py", "this free-boundary derivation gate"),
    ]
    return [
        {"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"}
        for path, role in sources
    ]


def shape_derivative_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "S1_domain_average",
            "formula": "<f>_D = V_D^-1 integral_D f dV",
            "result": "definition",
            "meaning": "all domain quantities are moving-boundary averages",
        },
        {
            "step": "S2_boundary_displacement",
            "formula": "delta_eta V_D = integral_boundaryD eta dSigma",
            "result": "standard_shape_variation",
            "meaning": "eta is outward normal boundary displacement",
        },
        {
            "step": "S3_average_variation",
            "formula": "delta_eta <f>_D = V_D^-1 integral_boundaryD eta (f-<f>_D) dSigma",
            "result": "derived_for_fixed_fields",
            "meaning": "boundary adds local value minus current mean",
        },
        {
            "step": "S4_Ccoh_variables",
            "formula": "a=<theta>_D, b=<R>_D, R=theta^2+sigma^2+omega^2+eps_D",
            "result": "definition",
            "meaning": "C_coh=a^2/b",
        },
        {
            "step": "S5_Ccoh_shape_derivative",
            "formula": "delta C = V_D^-1 integral_boundaryD eta[(2a/b)(theta-a)-(a^2/b^2)(R-b)] dSigma",
            "result": "derived",
            "meaning": "explicit free-boundary first variation",
        },
        {
            "step": "S6_unconstrained_Euler_condition",
            "formula": "(2a/b)(theta-a)-(a^2/b^2)(R-b)=0 on boundary",
            "result": "derived_if_eta_arbitrary",
            "meaning": "pointwise boundary stationarity condition",
        },
        {
            "step": "S7_volume_constrained_condition",
            "formula": "(2a/b)(theta-a)-(a^2/b^2)(R-b)=lambda on boundary",
            "result": "derived_if_volume_fixed",
            "meaning": "same equation with Lagrange multiplier for fixed volume",
        },
    ]


def euler_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "case": "nonzero_a_unconstrained",
            "condition": "2b(theta-a)-a(R-b)=0 on boundary",
            "selection_power": "weak",
            "issue": "boundary points must satisfy a coherence balance but this does not choose connected component uniquely",
        },
        {
            "case": "nonzero_a_fixed_volume",
            "condition": "2b(theta-a)-a(R-b)=lambda b^2/a on boundary",
            "selection_power": "weaker",
            "issue": "lambda encodes a supplied volume/normalization constraint",
        },
        {
            "case": "a_equals_zero",
            "condition": "delta C=0 at first order",
            "selection_power": "degenerate",
            "issue": "stationary/shear/virial domains become extremal but not selected",
        },
        {
            "case": "homogeneous_FLRW",
            "condition": "theta=a and R=b everywhere",
            "selection_power": "degenerate",
            "issue": "every homogeneous comoving domain is extremal; no boundary uniqueness",
        },
        {
            "case": "need_second_variation",
            "condition": "second variation distinguishes maxima/saddles only after D class and constraints are supplied",
            "selection_power": "not_enough",
            "issue": "parent action still needed to define admissible domains and boundary exchange",
        },
    ]


def branch_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "FLRW",
            "input": "theta constant, sigma=0, omega=0",
            "euler_readout": "boundary integrand zero",
            "verdict": "stationary_but_not_unique",
        },
        {
            "branch": "Minkowski_or_inertial_local",
            "input": "theta=0, sigma=0, omega=0",
            "euler_readout": "a=0 degeneracy",
            "verdict": "silent_but_not_selected",
        },
        {
            "branch": "stationary_bound_system",
            "input": "time-averaged <theta>_D=0 with possible shear/orbital motion",
            "euler_readout": "a=0 first-variation degeneracy",
            "verdict": "conditional_local_silence_not_domain_derivation",
        },
        {
            "branch": "tracefree_shear",
            "input": "theta=0, sigma nonzero",
            "euler_readout": "C_coh=0 and first variation degenerate",
            "verdict": "shear_not_selected_into_scalar_channel",
        },
        {
            "branch": "collapse_or_merger",
            "input": "nonzero inhomogeneous theta and R",
            "euler_readout": "boundary balance condition nontrivial",
            "verdict": "dynamic_activation_open",
        },
        {
            "branch": "virialized_galaxy",
            "input": "mean expansion approximately zero after averaging",
            "euler_readout": "degenerate local scalar channel; galaxy pillar must remain separate",
            "verdict": "not_a_parent_binding_derivation",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "shape_derivative_derived",
            "result": "yes",
            "evidence": "delta<f> formula gives explicit boundary integrand for delta C_coh",
            "claim_effect": "boundary problem is now mathematical, not vague",
        },
        {
            "gate": "free_boundary_Euler_equation_derived",
            "result": "yes",
            "evidence": "arbitrary eta gives integrand zero or lambda-constrained variant",
            "claim_effect": "candidate domain stationarity condition exists",
        },
        {
            "gate": "FLRW_selected",
            "result": "no_unique_selection",
            "evidence": "homogeneous FLRW makes every comoving domain stationary",
            "claim_effect": "needs parent domain class/current",
        },
        {
            "gate": "stationary_local_selected",
            "result": "no_unique_selection",
            "evidence": "a=<theta>=0 makes first variation vanish degenerately",
            "claim_effect": "local silence remains conditional",
        },
        {
            "gate": "quiet_domain_hand_choice_removed",
            "result": "not_yet",
            "evidence": "Euler equation admits many stationary domains and does not pick physical boundary",
            "claim_effect": "domain remains closure/theorem target",
        },
        {
            "gate": "new_scale_or_surface_tension_needed",
            "result": "only_if_uniqueness_demanded",
            "evidence": "area/compactness regularizers could select but would add scale/stress",
            "claim_effect": "do not add without parent derivation",
        },
        {
            "gate": "support_claim_allowed",
            "result": "no",
            "evidence": "domain class, boundary exchange, u3, Bmem, and matter coupling remain underived",
            "claim_effect": "no local-GR/unification promotion",
        },
    ]


def route_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "continue_derivation",
            "next_work": "derive admissible domain class and boundary current so Euler degeneracy is broken by topology/Noether data",
            "allowed": "yes",
            "risk": "may still collapse to closure if boundary current is chosen by outcome",
        },
        {
            "route": "add_surface_tension_or_length",
            "next_work": "regularize domain with area/perimeter/gradient penalty",
            "allowed": "no_without_parent_origin",
            "risk": "introduces local stress and fitted scale",
        },
        {
            "route": "empirical_closure_tests",
            "next_work": "test fixed-D/Qcoh branch as explicit effective closure",
            "allowed": "yes_with_labels",
            "risk": "not evidence of parent local-GR derivation",
        },
        {
            "route": "claim_domain_derived",
            "next_work": "promote local-GR branch",
            "allowed": "no",
            "risk": "Euler equation is stationary but not selecting",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The free-boundary variation of C_coh[D] is derived explicitly. "
                "It gives a real Euler condition, but the condition is degenerate in the exact branches we need most: homogeneous FLRW and stationary local domains are stationary without being uniquely selected. "
                "Therefore the derivation sharpens the domain problem but does not solve it; a parent admissible-domain/boundary-current principle is still required."
            ),
            "next_target": "derive_admissible_domain_class_or_boundary_current_that_breaks_Euler_degeneracy_without_new_scale",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "shape_derivative.csv": (shape_derivative_rows(), ["step", "formula", "result", "meaning"]),
        "euler_conditions.csv": (euler_condition_rows(), ["case", "condition", "selection_power", "issue"]),
        "branch_tests.csv": (branch_test_rows(), ["branch", "input", "euler_readout", "verdict"]),
        "gate_results.csv": (gate_rows(), ["gate", "result", "evidence", "claim_effect"]),
        "route_policy.csv": (route_policy_rows(), ["route", "next_work", "allowed", "risk"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "shape_derivative_derived": True,
        "free_boundary_Euler_equation_derived": True,
        "domain_uniquely_selected": False,
        "FLRW_stationary_not_unique": True,
        "stationary_local_degenerate": True,
        "quiet_domain_hand_choice_removed": False,
        "support_claim_allowed": False,
        "next_target": "derive_admissible_domain_class_or_boundary_current_that_breaks_Euler_degeneracy_without_new_scale",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Free-boundary Euler equation for C_coh[D].")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
