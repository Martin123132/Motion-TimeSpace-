from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "quotient-configuration-principle-from-topological-projector"
STATUS = "quotient_principle_conditionally_derived_from_presymplectic_topological_projector_Cperp_exactness_open"
CLAIM_CEILING = "quotient_principle_internal_only_no_local_GR_or_unification_promotion"

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
        (ROOT / "207-domain-projector-action-and-Bianchi-identity.md", "domain projector and Bianchi accounting"),
        (ROOT / "252-topological-projector-parent-action-skeleton.md", "topological projector parent skeleton"),
        (ROOT / "253-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure.md", "same-projector FLRW shape bridge"),
        (ROOT / "271-parent-no-Cperp-action-or-closure.md", "quotient-action skeleton"),
        (ROOT / "scripts" / "quotient_configuration_principle_from_topological_projector.py", "this quotient principle gate"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
        }
        for path, role in sources
    ]


def presymplectic_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Use a metric-independent relative/topological projector P_D.",
            "mathematical_form": "P_D^2=P_D, d_rel P_D=P_D d_rel, delta_g P_D=0",
            "status": "conditional_previous",
            "consequence": "projector can be treated as chain/class data rather than local Hodge dynamics",
        },
        {
            "step": 2,
            "statement": "Define the physical C variable as its projected class.",
            "mathematical_form": "C_phys = [C] = P_D C = C_D",
            "status": "candidate",
            "consequence": "raw Cperp lies in ker(P_D)",
        },
        {
            "step": 3,
            "statement": "Require residual shifts to be relative-exact representatives.",
            "mathematical_form": "delta_eta Cperp = eta_perp, P_D eta_perp=0, eta_perp=d_rel alpha or relative-trivial",
            "status": "open_burden",
            "consequence": "compact local residuals can be gauge if boundary primitive is pure gauge",
        },
        {
            "step": 4,
            "statement": "Topological action changes by a boundary term under exact residual shifts.",
            "mathematical_form": "delta_eta S_top = integral_D d_rel(... eta_perp ...) = integral_boundaryD ...",
            "status": "conditional_pass_if_step3",
            "consequence": "stationary/relative boundary conditions annihilate compact local residual variation",
        },
        {
            "step": 5,
            "statement": "Presymplectic potential has no bulk pairing with eta_perp.",
            "mathematical_form": "Theta(eta_perp)=boundary or 0, Omega(eta_perp,delta)=0",
            "status": "conditional_pass_if_step3",
            "consequence": "eta_perp is a null direction of the presymplectic form",
        },
        {
            "step": 6,
            "statement": "Reduced phase space quotients by the null direction.",
            "mathematical_form": "Phase_phys = ConstraintSurface / ker(Omega), C ~ C+eta_perp",
            "status": "conditional_derivation",
            "consequence": "physical configuration space is [C]=C/ker(P_D)",
        },
        {
            "step": 7,
            "statement": "Matter metric selector follows from quotient invariance.",
            "mathematical_form": "bar_g=exp(F[C])g, F[C+eta_perp]=F[C] -> F=P_D C",
            "status": "conditional_previous",
            "consequence": "projected matter metric is selected if quotient is real",
        },
    ]


def exactness_requirements_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement": "E1_C_sector_topological_not_scalar",
            "required_form": "C residual enters only through relative/topological class data, not ordinary scalar kinetic terms",
            "current_status": "not_derived",
            "failure_if_absent": "Cperp is a physical scalar",
        },
        {
            "requirement": "E2_Cperp_relative_exact",
            "required_form": "Cperp local residuals lie in exact/trivial relative class after mass/shear/ordinary flux projection",
            "current_status": "supported_by_231_analogy_not_proven_for_C",
            "failure_if_absent": "ker(P_D) may contain physical local hair",
        },
        {
            "requirement": "E3_boundary_primitive_zero_local",
            "required_form": "stationary compact/local domains have pure-gauge boundary primitive",
            "current_status": "contract_from_60_not_derived",
            "failure_if_absent": "Stokes boundary term can source observables",
        },
        {
            "requirement": "E4_FLRW_boundary_nonzero",
            "required_form": "coherent FLRW domain retains nontrivial projected class",
            "current_status": "conditional_shape_bridge_from_253",
            "failure_if_absent": "same quotient kills cosmological memory",
        },
        {
            "requirement": "E5_domain_variation",
            "required_form": "domain labels, weights, and boundaries varied with stress retained",
            "current_status": "open",
            "failure_if_absent": "external projector masquerades as gauge",
        },
        {
            "requirement": "E6_no_Hodge_projector",
            "required_form": "P_D is relative-chain/topological, not metric/Hodge least-energy",
            "current_status": "conditional_previous",
            "failure_if_absent": "projector creates metric stress and representative dynamics",
        },
        {
            "requirement": "E7_FLRW_amplitude",
            "required_form": "same quotient/projector derives B_mem=2/27 or keeps closure",
            "current_status": "not_derived",
            "failure_if_absent": "no amplitude promotion",
        },
    ]


def boundary_case_rows() -> list[dict[str, Any]]:
    return [
        {
            "case": "compact_stationary_local_domain",
            "boundary_condition": "relative boundary primitive pure gauge; no coherent expansion class",
            "quotient_result": "Cperp exact shifts are null",
            "status": "conditional_pass",
        },
        {
            "case": "local_exterior_shell_after_mass_projection",
            "boundary_condition": "ordinary H^2 mass flux separated as M_eff; memory residual relative class trivial",
            "quotient_result": "supports exact Cperp analogy",
            "status": "supporting_not_proven_for_C",
        },
        {
            "case": "FLRW_coherent_domain",
            "boundary_condition": "nontrivial coherent expansion class survives",
            "quotient_result": "C_D can remain cosmological",
            "status": "conditional_shape_only",
        },
        {
            "case": "dynamic_boundary_merger_or_wall",
            "boundary_condition": "boundary primitive may be nonzero",
            "quotient_result": "not safe to quotient without transition law",
            "status": "open",
        },
        {
            "case": "BAO_smooth_subdomain",
            "boundary_condition": "treated inside predeclared Hubble-cap coherent domain",
            "quotient_result": "same-domain projected metric can preserve common-mode cancellation",
            "status": "conditional_previous",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "topological_presymplectic_route",
            "result": "conditional_pass",
            "evidence": "exact residual shifts are null directions if action is topological/relative and boundary term vanishes",
            "claim_effect": "quotient principle has a real theorem shape",
        },
        {
            "gate": "Cperp_exactness_for_C_sector",
            "result": "not_derived",
            "evidence": "cohomology exactness is proven for J_rel-style memory current, not yet for Cperp scalar/representative",
            "claim_effect": "no parent promotion",
        },
        {
            "gate": "boundary_conditions",
            "result": "partial",
            "evidence": "local-zero/FLRW-nonzero boundary contract exists but remains theorem target",
            "claim_effect": "quotient branch remains conditional",
        },
        {
            "gate": "Hamiltonian_Cperp_independence",
            "result": "conditional_pass_if_exactness",
            "evidence": "presymplectic null direction implies no physical Hamiltonian dependence",
            "claim_effect": "solves no-Cperp action only under exactness assumptions",
        },
        {
            "gate": "projected_metric_selector",
            "result": "conditional_pass",
            "evidence": "quotient invariance forces F[C]=P_D C",
            "claim_effect": "selector remains serious theorem target",
        },
        {
            "gate": "FLRW_unification_and_Bmem",
            "result": "open",
            "evidence": "same projector gives shape route but not B_mem=2/27",
            "claim_effect": "no unification or amplitude claim",
        },
        {
            "gate": "closure_policy",
            "result": "explicit",
            "evidence": "if Cperp exactness / quotient principle fails, projected metric is closure",
            "claim_effect": "prevents silent overclaim",
        },
        {
            "gate": "support_claim_allowed",
            "result": "no",
            "evidence": "Cperp exactness, boundary theorem, domain variation, and Bmem remain open",
            "claim_effect": "no local-GR or unification promotion",
        },
    ]


def comparison_rows() -> list[dict[str, Any]]:
    return [
        {
            "question": "Does topological projector derive quotient in principle?",
            "answer": "yes_conditionally",
            "evidence": "topological exact shifts are presymplectic null directions",
            "status": "conditional_theorem_shape",
        },
        {
            "question": "Is Cperp proven to be such an exact shift?",
            "answer": "no",
            "evidence": "Cperp exactness has not been derived from parent C-sector",
            "status": "main_failure",
        },
        {
            "question": "Does this improve over checkpoint 271?",
            "answer": "yes",
            "evidence": "quotient is no longer pure axiom; it has a sufficient presymplectic/topological route",
            "status": "progress",
        },
        {
            "question": "Can projected metric be promoted?",
            "answer": "no",
            "evidence": "exactness, boundary, FLRW amplitude, and domain variation are still open",
            "status": "no_promotion",
        },
        {
            "question": "What if exactness fails?",
            "answer": "closure",
            "evidence": "then exp(P_D C)g is imposed effective coupling",
            "status": "explicit_demote_path",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The quotient configuration principle has a conditional topological/presymplectic derivation route: "
                "if Cperp residuals are relative-exact representatives with vanishing local boundary primitive, they are null directions of the presymplectic form, so the physical configuration space is the quotient [C]=C/ker(P_D). "
                "But Cperp exactness for the C-sector is not yet parent-derived, so projected matter metric remains a theorem target, not a promotion."
            ),
            "next_target": "derive_Cperp_relative_exactness_for_C_sector_or_label_projected_metric_as_closure",
        }
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
            "meaning": "residual Cperp matter leak bound if quotient fails",
        },
        {
            "quantity": "epsilon_local_qR_max",
            "value": LOCAL_QR_GATE / B_MEM,
            "meaning": "stricter local qR-like leak bound if quotient fails",
        },
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "presymplectic_quotient_chain.csv": (
            presymplectic_chain_rows(),
            ["step", "statement", "mathematical_form", "status", "consequence"],
        ),
        "exactness_requirements.csv": (
            exactness_requirements_rows(),
            ["requirement", "required_form", "current_status", "failure_if_absent"],
        ),
        "boundary_cases.csv": (boundary_case_rows(), ["case", "boundary_condition", "quotient_result", "status"]),
        "gate_results.csv": (gate_rows(), ["gate", "result", "evidence", "claim_effect"]),
        "derivation_vs_closure.csv": (comparison_rows(), ["question", "answer", "evidence", "status"]),
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
        "topological_presymplectic_quotient_route": True,
        "Cperp_exactness_for_C_sector_derived": False,
        "quotient_principle_promoted": False,
        "projected_metric_promoted": False,
        "local_GR_or_unification_claim_allowed": False,
        "next_target": "derive_Cperp_relative_exactness_for_C_sector_or_label_projected_metric_as_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(status + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Quotient configuration principle from topological projector gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
