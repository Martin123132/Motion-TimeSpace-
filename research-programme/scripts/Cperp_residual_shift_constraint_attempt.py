from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "Cperp-residual-shift-constraint-attempt"
STATUS = "Cperp_residual_shift_first_class_route_conditionally_consistent_parent_no_Cperp_action_missing"
CLAIM_CEILING = "Cperp_constraint_internal_only_no_local_GR_or_unification_promotion"

B_MEM = 2.0 / 27.0
LOCAL_DELTA_C_GATE = 4.6e-05
LOCAL_QR_GATE = 2.3e-05


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
        (ROOT / "269-metric-selector-principle-attempt.md", "metric selector principle and residual gauge burden"),
        (ROOT / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md", "first-order multiplier precedent"),
        (ROOT / "231-Jrel-cohomology-projector-or-local-EH-limit.md", "relative cohomology exactness precedent"),
        (ROOT / "207-domain-projector-action-and-Bianchi-identity.md", "projector action and Bianchi accounting"),
        (ROOT / "268-projected-matter-metric-parent-action-or-closure.md", "projected matter metric skeleton"),
        (ROOT / "scripts" / "Cperp_residual_shift_constraint_attempt.py", "this first-class constraint attempt"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
        }
        for path, role in sources
    ]


def constraint_algebra_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "field_split",
            "formula": "C = C_D + Cperp, P_D Cperp = 0",
            "role": "decomposes coherent zero mode and residual representative",
            "status": "conditional_previous",
        },
        {
            "object": "gauge_parameter",
            "formula": "eta_perp with P_D eta_perp = 0",
            "role": "allowed residual shift parameter",
            "status": "definition",
        },
        {
            "object": "candidate_generator",
            "formula": "G[eta] = integral pi_perp eta_perp",
            "role": "generates delta Cperp = eta_perp",
            "status": "canonical_candidate",
        },
        {
            "object": "primary_constraint",
            "formula": "pi_perp(x) approx 0 on the P_perp subspace",
            "role": "removes Cperp momentum and starts zero-dof route",
            "status": "required",
        },
        {
            "object": "self_bracket",
            "formula": "{G[eta], G[xi]} = 0",
            "role": "Abelian residual-shift algebra",
            "status": "conditional_pass",
        },
        {
            "object": "Hamiltonian_bracket",
            "formula": "{G[eta], H} = - integral eta_perp delta H / delta Cperp",
            "role": "tests whether residual shift is first-class",
            "status": "pass_only_if_H_independent_of_Cperp",
        },
        {
            "object": "preservation_condition",
            "formula": "delta H / delta Cperp approx 0",
            "role": "no Cperp potential, gradient, kinetic, matter, or source term outside constraints",
            "status": "parent_action_missing",
        },
        {
            "object": "diffeomorphism_bracket",
            "formula": "{G[eta], H_diff[N]} closes if P_D/domain labels are varied consistently",
            "role": "prevents projector from being an external noncovariant structure",
            "status": "conditional_open",
        },
    ]


def first_class_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "F1_no_Cperp_matter_metric",
            "required_form": "S_matter[psi, exp(P_D C)g]",
            "status": "conditional_previous",
            "failure_if_absent": "Cperp trace source returns",
        },
        {
            "condition": "F2_no_Cperp_kinetic_term",
            "required_form": "no dot(Cperp)^2 or invertible kinetic matrix for Cperp",
            "status": "not_parent_derived",
            "failure_if_absent": "pi_perp is not a constraint",
        },
        {
            "condition": "F3_no_Cperp_gradient_stiffness",
            "required_form": "no (nabla Cperp)^2 physical energy except gauge-fixing/exact boundary terms",
            "status": "not_parent_derived",
            "failure_if_absent": "Cperp becomes local scalar/hair",
        },
        {
            "condition": "F4_no_Cperp_potential",
            "required_form": "V depends on C_D or class variables, not Cperp representative",
            "status": "not_parent_derived",
            "failure_if_absent": "residual shift is explicitly broken",
        },
        {
            "condition": "F5_relative_exact_boundary",
            "required_form": "compact local Cperp lies in exact/relative trivial class with pure-gauge boundary primitive",
            "status": "conditional_cohomology_support",
            "failure_if_absent": "local representative may be observable",
        },
        {
            "condition": "F6_projector_action_owned",
            "required_form": "P_D arises from varied domain variables and retained stresses",
            "status": "conditional_previous",
            "failure_if_absent": "external average masquerades as gauge",
        },
        {
            "condition": "F7_domain_scale_predeclared",
            "required_form": "L_D or L_cg selected before empirical scoring",
            "status": "open",
            "failure_if_absent": "local silence/domain scale looks tuned",
        },
    ]


def dof_count_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "first_class_Cperp",
            "canonical_variables": "Cperp, pi_perp",
            "constraints": "one first-class constraint pi_perp approx 0 plus gauge orbit Cperp -> Cperp+eta_perp",
            "local_dof": 0,
            "verdict": "conditional_pass_if_F1_F7",
        },
        {
            "branch": "second_class_or_heavy_Cperp",
            "canonical_variables": "Cperp, pi_perp",
            "constraints": "stiff equations or second-class pair",
            "local_dof": "0_or_1_effective",
            "verdict": "not_lead; needs extreme local suppression",
        },
        {
            "branch": "ordinary_scalar_Cperp",
            "canonical_variables": "Cperp, pi_perp",
            "constraints": "none",
            "local_dof": 1,
            "verdict": "rejected_as_lead",
        },
        {
            "branch": "closure_projected_metric",
            "canonical_variables": "C_D only in matter metric",
            "constraints": "selector imposed, not derived",
            "local_dof": "not_parent_counted",
            "verdict": "allowed_only_if_labelled_closure",
        },
    ]


def cohomology_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "piece": "local_shell_exactness",
            "input": "compact exterior shell with relative class trivial after mass/shear projection",
            "borrowed_from": "231-Jrel cohomology gate",
            "use_for_Cperp": "supports treating compact residual memory representative as exact",
            "status": "supporting_not_sufficient",
        },
        {
            "piece": "absolute_mass_flux_separation",
            "input": "ordinary H^2 mass/Gauss flux must remain M_eff, not memory residual",
            "borrowed_from": "231-Jrel cohomology gate",
            "use_for_Cperp": "prevents selector from deleting ordinary gravity",
            "status": "required",
        },
        {
            "piece": "FLRW_nonzero_class",
            "input": "coherent expanding domain carries nontrivial class",
            "borrowed_from": "60-relative boundary contract",
            "use_for_Cperp": "keeps C_D cosmological while local residual is exact",
            "status": "contract_not_derived",
        },
        {
            "piece": "matter_observables_on_quotient",
            "input": "observables depend on relative class, not exact representative",
            "borrowed_from": "new selector requirement",
            "use_for_Cperp": "would justify exp(P_D C)g",
            "status": "not_parent_derived",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "candidate_shift_generator",
            "result": "conditional_pass",
            "evidence": "G[eta]=int pi_perp eta gives delta Cperp=eta_perp",
            "claim_effect": "first-class route is mathematically available",
        },
        {
            "gate": "self_algebra",
            "result": "pass",
            "evidence": "{G[eta],G[xi]}=0",
            "claim_effect": "residual shift is Abelian at this level",
        },
        {
            "gate": "Hamiltonian_invariance",
            "result": "not_derived",
            "evidence": "requires delta H/delta Cperp approx 0",
            "claim_effect": "parent action must contain no physical Cperp dependence",
        },
        {
            "gate": "relative_exact_support",
            "result": "partial",
            "evidence": "local shell cohomology supports exact residual classes after mass/shear projection",
            "claim_effect": "supports route but does not prove first-class parent constraint",
        },
        {
            "gate": "ordinary_scalar_Cperp",
            "result": "rejected_as_lead",
            "evidence": "would create local matter-coupled hair unless epsilon is tiny",
            "claim_effect": "do not treat Cperp as ordinary local field",
        },
        {
            "gate": "metric_selector_parent_promotion",
            "result": "blocked",
            "evidence": "F2-F4 parent no-Cperp action not derived",
            "claim_effect": "selector remains theorem target / closure candidate",
        },
        {
            "gate": "support_claim_allowed",
            "result": "no",
            "evidence": "first-class constraint and parent projector not fully derived",
            "claim_effect": "no local-GR or unification promotion",
        },
    ]


def numeric_rows() -> list[dict[str, Any]]:
    return [
        {
            "quantity": "B_mem",
            "value": B_MEM,
            "meaning": "fixed closure/theorem target carried forward",
        },
        {
            "quantity": "epsilon_local_DeltaC_max",
            "value": LOCAL_DELTA_C_GATE / B_MEM,
            "meaning": "if residual Cperp leaks into matter coupling, local Delta C gate requires below this",
        },
        {
            "quantity": "epsilon_local_qR_max",
            "value": LOCAL_QR_GATE / B_MEM,
            "meaning": "stricter local qR-like residual-coupling bound",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "Cperp residual shift can be a first-class redundancy only if pi_perp≈0 is preserved by a parent Hamiltonian "
                "with no physical Cperp dependence. The algebraic route is consistent and supported by relative-exact local cohomology, "
                "but the parent no-Cperp action principle is not derived. The selector remains a theorem target, not a promotion."
            ),
            "next_target": "construct_parent_no_Cperp_action_or_demote_projected_metric_selector_to_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "constraint_algebra.csv": (constraint_algebra_rows(), ["object", "formula", "role", "status"]),
        "first_class_conditions.csv": (first_class_condition_rows(), ["condition", "required_form", "status", "failure_if_absent"]),
        "dof_count.csv": (dof_count_rows(), ["branch", "canonical_variables", "constraints", "local_dof", "verdict"]),
        "cohomology_bridge.csv": (cohomology_bridge_rows(), ["piece", "input", "borrowed_from", "use_for_Cperp", "status"]),
        "gate_results.csv": (gate_rows(), ["gate", "result", "evidence", "claim_effect"]),
        "numeric_bounds.csv": (numeric_rows(), ["quantity", "value", "meaning"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status = decision_rows()[0]["decision"]
    payload = {
        "status": status,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "candidate_shift_generator_defined": True,
        "self_algebra_closes": True,
        "Hamiltonian_Cperp_independence_derived": False,
        "first_class_Cperp_constraint_promoted": False,
        "ordinary_scalar_Cperp_rejected_as_lead": True,
        "local_GR_or_unification_claim_allowed": False,
        "next_target": "construct_parent_no_Cperp_action_or_demote_projected_metric_selector_to_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(status + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Cperp residual-shift first-class constraint attempt.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
