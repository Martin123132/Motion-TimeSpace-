from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "coherent-domain-projector-from-parent-variables"
STATUS = "fixed_D_Qcoh_projection_mathematically_derived_domain_selector_not_parent_derived"
CLAIM_CEILING = "coherent_projection_sharpened_domain_selection_open_no_local_GR_promotion"


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
        (ROOT / "64-binding-invariant-domain-selector-attempt.md", "coherent-volume-flow invariant"),
        (ROOT / "68-chiD-gated-memory-conservation-contract.md", "gated memory conservation/Bianchi contract"),
        (ROOT / "142-domain-load-tensor-owner-promotion-gate.md", "Q reduced to coherent-volume load if D/u3 owned"),
        (ROOT / "143-domain-selector-variational-action-attempt.md", "zero-knob domain selector failure/open boundary terms"),
        (ROOT / "275-JC-three-form-memory-current-from-Q.md", "J_C requires parent-owned D and Q_coh"),
        (ROOT / "scripts" / "coherent_domain_projector_from_parent_variables.py", "this coherent projector gate"),
    ]
    return [
        {"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"}
        for path, role in sources
    ]


def fixed_domain_projection_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "input_object",
            "formula": "Q^i_j(x) on a chosen spatial domain D",
            "status": "parent_variable_assumed_from_previous_Q_route",
            "meaning": "accumulated expansion/load tensor before FLRW symmetry",
        },
        {
            "item": "projection_subspace",
            "formula": "S_D = { q delta^i_j : q constant over D }",
            "status": "mathematical_definition",
            "meaning": "coherent isotropic volume-load subspace",
        },
        {
            "item": "least_square_functional",
            "formula": "E_D(q)=<||Q-qI||^2>_D",
            "status": "mathematical_projection",
            "meaning": "orthogonal projection of Q onto coherent isotropic subspace",
        },
        {
            "item": "Euler_condition",
            "formula": "dE_D/dq=0 => q=(1/3)<Tr Q>_D",
            "status": "derived_for_fixed_D",
            "meaning": "no hand choice of Q_coh once D and inner product are given",
        },
        {
            "item": "coherent_projector",
            "formula": "P_coh[Q]^i_j=(1/3)<Tr Q>_D delta^i_j",
            "status": "derived_for_fixed_D",
            "meaning": "tracefree shear is orthogonal to the retained channel",
        },
        {
            "item": "FLRW_reduction",
            "formula": "Q=(N/u3)I => P_coh[Q]=Q",
            "status": "pass",
            "meaning": "FLRW branch unaffected",
        },
        {
            "item": "stationary_local_reduction",
            "formula": "<Tr Q>_D=0 => P_coh[Q]=0",
            "status": "conditional_pass",
            "meaning": "local scalar memory off for stable-volume domains",
        },
    ]


def domain_selector_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "external_smoothing_domain",
            "definition": "choose D by observational convenience or fitted scale",
            "passes_nonimport": "no",
            "issue": "rescue knob",
            "verdict": "rejected",
        },
        {
            "candidate": "maximal_connected_coherent_flow_domain",
            "definition": "largest connected positive/negative volume-flow region with high C_coh",
            "passes_nonimport": "partial",
            "issue": "maximal rule not Euler-derived",
            "verdict": "best_contract_not_derivation",
        },
        {
            "candidate": "coherence_quotient_extremal",
            "definition": "extremize C_coh[D]=<theta>_D^2/(<theta^2>_D+<sigma^2>_D+<omega^2>_D+eps_D)",
            "passes_nonimport": "partial",
            "issue": "free-boundary condition and eps_D still need parent origin",
            "verdict": "best_variational_theorem_target",
        },
        {
            "candidate": "chiD_auxiliary_selector",
            "definition": "chi_D constrained to C_coh[D] or related class variable",
            "passes_nonimport": "partial",
            "issue": "can classify domain but not select support by itself",
            "verdict": "useful_auxiliary_not_domain_owner",
        },
        {
            "candidate": "relative_boundary_current",
            "definition": "select trivial/nontrivial relative memory class by boundary current equation",
            "passes_nonimport": "partial",
            "issue": "boundary primitive theorem still missing",
            "verdict": "needed_for_exactness_not_selector",
        },
    ]


def variational_boundary_rows() -> list[dict[str, Any]]:
    return [
        {
            "variation": "fixed_D_Q_projection",
            "result": "closed",
            "equation": "d/dq <||Q-qI||^2>_D=0",
            "open_piece": "none for fixed D",
        },
        {
            "variation": "move_boundary_of_D",
            "result": "open",
            "equation": "delta_D C_coh[D] = bulk average terms + boundary integrand mismatch",
            "open_piece": "parent condition that sets physical boundary",
        },
        {
            "variation": "chiD_auxiliary",
            "result": "conditional",
            "equation": "E_lambda=0 -> chi_D=C_coh[D]",
            "open_piece": "support/level-set selection and boundary stress",
        },
        {
            "variation": "Bianchi_conservation",
            "result": "open",
            "equation": "nabla_mu T_total^munu = sum E_field L_xi(field)",
            "open_piece": "full on-shell selector/domain stress cancellation",
        },
    ]


def branch_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "FLRW",
            "projector_readout": "P_coh[Q]=Q=(N/u3)I",
            "domain_status": "homogeneous domain plausible",
            "verdict": "pass_conditional",
        },
        {
            "branch": "Minkowski_or_inertial_patch",
            "projector_readout": "<Tr Q>_D=0",
            "domain_status": "stable local domain plausible",
            "verdict": "pass_conditional",
        },
        {
            "branch": "stationary_solar_system",
            "projector_readout": "stable-volume D gives P_coh[Q]=0",
            "domain_status": "needs parent bound-domain theorem",
            "verdict": "conditional_not_promoted",
        },
        {
            "branch": "tracefree_shear_or_GW",
            "projector_readout": "Tr S=0 is removed by fixed-D projection",
            "domain_status": "dynamic boundary/backreaction open",
            "verdict": "projection_pass_domain_open",
        },
        {
            "branch": "collapse_or_merger",
            "projector_readout": "coherent trace can activate",
            "domain_status": "not safe to force silent",
            "verdict": "open_dynamic_branch",
        },
        {
            "branch": "virialized_galaxy",
            "projector_readout": "time-averaged <theta> may vanish while nonlocal/galaxy pillar remains separate",
            "domain_status": "risk of importing Newtonian binding",
            "verdict": "open_conditional",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "fixed_D_Qcoh_projection_derived",
            "result": "yes",
            "evidence": "least-squares/orthogonal projection gives q=(1/3)<Tr Q>_D",
            "claim_effect": "Q_coh no longer arbitrary once D is supplied",
        },
        {
            "gate": "tracefree_shear_removed_from_JC",
            "result": "yes_for_projected_Qcoh",
            "evidence": "tracefree part orthogonal to isotropic coherent subspace",
            "claim_effect": "repairs 275 unprojected determinant leak conditionally",
        },
        {
            "gate": "domain_D_parent_selected",
            "result": "no",
            "evidence": "coherence quotient/free-boundary rule remains theorem target",
            "claim_effect": "local-GR promotion still blocked",
        },
        {
            "gate": "projection_norm_parent_derived",
            "result": "not_fully",
            "evidence": "quadratic Hilbert projection is natural but not yet obtained from parent action",
            "claim_effect": "projection is mathematical, physical ownership conditional",
        },
        {
            "gate": "boundary_stress_closed",
            "result": "no",
            "evidence": "moving-domain variation and chi_D stress remain open",
            "claim_effect": "Bianchi/conservation not promoted",
        },
        {
            "gate": "support_claim_allowed",
            "result": "no",
            "evidence": "D selector, boundary primitive, u3, Bmem, and matter coupling remain underived",
            "claim_effect": "no local-GR/unification promotion",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "For a fixed physical domain D, the coherent projector is mathematically derived: P_coh[Q]=(1/3)<Tr Q>_D I is the orthogonal least-squares projection of Q onto the isotropic coherent volume-load subspace. "
                "This removes tracefree-shear leakage from J_C when the projected branch is used. "
                "The physical domain selector D is still not parent-derived; coherence extremization is only a variational theorem target with open boundary/Bianchi terms."
            ),
            "next_target": "derive_domain_D_free_boundary_Euler_equation_or_keep_domain_as_closure",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "fixed_domain_projection.csv": (fixed_domain_projection_rows(), ["item", "formula", "status", "meaning"]),
        "domain_selector_candidates.csv": (
            domain_selector_rows(),
            ["candidate", "definition", "passes_nonimport", "issue", "verdict"],
        ),
        "variational_boundary_terms.csv": (
            variational_boundary_rows(),
            ["variation", "result", "equation", "open_piece"],
        ),
        "branch_tests.csv": (branch_test_rows(), ["branch", "projector_readout", "domain_status", "verdict"]),
        "gate_results.csv": (gate_rows(), ["gate", "result", "evidence", "claim_effect"]),
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
        "fixed_D_Qcoh_projection_derived": True,
        "Qcoh_formula": "P_coh[Q]^i_j=(1/3)<Tr Q>_D delta^i_j",
        "tracefree_shear_removed_by_projected_Qcoh": True,
        "domain_D_parent_selected": False,
        "projection_norm_parent_derived": False,
        "boundary_stress_closed": False,
        "support_claim_allowed": False,
        "next_target": "derive_domain_D_free_boundary_Euler_equation_or_keep_domain_as_closure",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Coherent-domain projector derivation gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
