#!/usr/bin/env python3
"""Attempt to derive the C2 p=3 activation law from a parent memory current."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "46_status": Path("runs/20260531-013929-activation-regularity-repair-gate/status.json"),
    "46_candidate_laws": Path("runs/20260531-013929-activation-regularity-repair-gate/results/candidate_activation_laws.csv"),
    "47_status": Path("runs/20260531-014459-C2-activation-background-smoke/status.json"),
    "48_status": Path("runs/20260531-015005-C2-activation-growth-CMB-retest/status.json"),
    "49_status": Path("runs/20260531-015400-C2-regularized-closure-ledger/status.json"),
    "49_missing_gates": Path("runs/20260531-015400-C2-regularized-closure-ledger/results/still_borrowed_missing_gates.csv"),
    "49_decision": Path("runs/20260531-015400-C2-regularized-closure-ledger/results/decision.csv"),
}

C2_CANDIDATE = "weibull_p3_match_N50"


def absolute_source(key: str) -> Path:
    return POST_CHECKPOINT / SOURCE_PATHS[key]


def load_json(key: str) -> dict[str, Any]:
    return json.loads(absolute_source(key).read_text(encoding="utf-8"))


def read_csv(key: str) -> list[dict[str, str]]:
    with absolute_source(key).open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def row_where(rows: list[dict[str, str]], **matches: str) -> dict[str, str]:
    for row in rows:
        if all(row.get(key) == value for key, value in matches.items()):
            return row
    raise ValueError(f"row not found: {matches}")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, relative_path in SOURCE_PATHS.items():
        absolute_path = POST_CHECKPOINT / relative_path
        rows.append(
            {
                "source_key": key,
                "relative_path": str(relative_path),
                "absolute_path": str(absolute_path),
                "exists": absolute_path.exists(),
            }
        )
    missing = [row["absolute_path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def activation_equation_rows(c2_law: dict[str, str]) -> list[dict[str, Any]]:
    u3 = float(c2_law["u_s"])
    n50 = float(c2_law["N50"])
    return [
        {
            "step": 1,
            "object": "activation_survival_form",
            "equation": "F(N)=1-exp[-I(N)]",
            "variables": "F activation fraction; I cumulative memory exposure",
            "derivation_status": "standard_if_memory_events_accumulate_as_survival_probability",
            "assumption": "activation is irreversible/saturating and exposure-additive",
            "source_or_value": "parent exposure ansatz, not yet parent action",
        },
        {
            "step": 2,
            "object": "dimensionless_load",
            "equation": "X_FLRW=N/u3",
            "variables": f"N=ln(1+z) or equivalent past-directed load; u3={u3}",
            "derivation_status": "not_parent_derived",
            "assumption": "FLRW has a scalar load coordinate proportional to N",
            "source_or_value": f"N50={n50}; u3 inherited from checkpoint-46 N50 match",
        },
        {
            "step": 3,
            "object": "minimal_C2_exposure",
            "equation": "I(N)=X_FLRW^3",
            "variables": "I exposure; X_FLRW dimensionless load",
            "derivation_status": "regularity_selected_not_parent_derived",
            "assumption": "lowest nonzero endpoint power with F(0)=F'(0)=F''(0)=0 and no extra continuous knob",
            "source_or_value": "checkpoint-46 regularity repair",
        },
        {
            "step": 4,
            "object": "memory_current",
            "equation": "J_M=dI/dN=3X_FLRW^2/u3=3N^2/u3^3",
            "variables": "J_M memory hazard/current per e-fold load",
            "derivation_status": "conditional_if_I_equals_X_cubed",
            "assumption": "parent memory current has a double zero at N=0",
            "source_or_value": f"u3={u3}",
        },
        {
            "step": 5,
            "object": "activation_dynamics",
            "equation": "dF/dN=(1-F)J_M=(1-F)3X_FLRW^2/u3",
            "variables": "F activation; J_M current",
            "derivation_status": "exact_given_survival_form_and_cubic_exposure",
            "assumption": "no separate decay/deactivation branch for past-directed N>=0",
            "source_or_value": "calculus identity",
        },
        {
            "step": 6,
            "object": "endpoint_series",
            "equation": "F=N^3/u3^3+O(N^6); F(0)=0; F'(0)=0; F''(0)=0; F'''(0)=6/u3^3",
            "variables": "endpoint derivatives of activation",
            "derivation_status": "exact_for_C2_weibull_p3",
            "assumption": "N approaches zero from the physical branch",
            "source_or_value": f"F'''(0)={6.0 / (u3 ** 3)}",
        },
    ]


def derivation_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "minimal_regular_endpoint_power",
            "claim": "p=3 is the lowest endpoint power compatible with C2 activation and finite canonical scalar-potential slope",
            "status": "partial_selection_not_parent_derivation",
            "passes": "selects p=3 over fractional p=1.7500073382761008 and over unnecessary p>3 if no extra smoothness is demanded",
            "fails": "does not explain why parent dynamics choose Weibull survival form or u3",
            "next_action": "derive the parent source/current whose first nonzero term is quadratic in FLRW load",
        },
        {
            "route": "quadratic_memory_hazard",
            "claim": "J_M is proportional to X_FLRW^2, giving I=X_FLRW^3 and F=1-exp[-X_FLRW^3]",
            "status": "conditional_route",
            "passes": "gives the required double zero and exact p=3 law",
            "fails": "J_M=3X_FLRW^2 dX_FLRW/dN is assumed rather than varied from a parent action",
            "next_action": "construct or reject a Noether/constraint reason for quadratic current onset",
        },
        {
            "route": "cubic_exposure_volume",
            "claim": "memory exposure counts a cubic coarse-grained phase/load volume",
            "status": "conditional_route",
            "passes": "naturally yields the cubic exponent without adding a fitted shape knob",
            "fails": "the relevant three-dimensional measure is unnamed and not tied to psi/Gamma/C/S_memory",
            "next_action": "identify the invariant volume element or demote this to analogy",
        },
        {
            "route": "local_double_zero_analogy",
            "claim": "the cosmology activation current has the same kind of double-zero silence demanded by local PPN suppression",
            "status": "analogy_not_derivation",
            "passes": "unifies a design principle: locally silent/cosmologically smooth branches require vanishing source and first derivative",
            "fails": "does not prove the same parent tensor controls local q_loc^nu and FLRW activation",
            "next_action": "write a shared current contract linking local and FLRW projections",
        },
        {
            "route": "direct_parent_action_variation",
            "claim": "vary a parent action and obtain the p=3 memory law directly",
            "status": "missing",
            "passes": "nothing yet",
            "fails": "no action term currently produces X_FLRW, J_M, u3, b_mem, and conservation together",
            "next_action": "define the minimal parent contract before more data scoring",
        },
    ]


def parent_contract_rows(c2_law: dict[str, str]) -> list[dict[str, Any]]:
    return [
        {
            "requirement": "define_X_FLRW",
            "needed_statement": "X_FLRW must be a dimensionless scalar projection of parent variables, not merely N/u3 by fit inheritance",
            "current_status": "missing",
            "failure_if_absent": "p=3 remains a regularized closure shape",
        },
        {
            "requirement": "derive_memory_current",
            "needed_statement": "J_M=3X_FLRW^2 dX_FLRW/dN must follow from continuity, constraint propagation, Noether current, or action variation",
            "current_status": "missing",
            "failure_if_absent": "the double zero is smuggled in",
        },
        {
            "requirement": "derive_transition_scale",
            "needed_statement": f"u3={c2_law['u_s']} and N50={c2_law['N50']} must be predicted or tied to a parent invariant",
            "current_status": "missing",
            "failure_if_absent": "transition scale remains borrowed from the old fractional closure",
        },
        {
            "requirement": "derive_b_mem",
            "needed_statement": "b_mem must arise from a memory stress amplitude, trace budget, coupling, or boundary condition",
            "current_status": "missing",
            "failure_if_absent": "cosmology amplitude remains calibrated closure",
        },
        {
            "requirement": "conservation_owner",
            "needed_statement": "Bianchi/conservation bookkeeping must say which sector carries the memory exchange",
            "current_status": "missing",
            "failure_if_absent": "background equations may be phenomenological rather than covariant",
        },
        {
            "requirement": "future_branch_time_arrow",
            "needed_statement": "odd p=3 is real for signed N but needs a parent branch rule so F does not become unphysical for future-directed N<0",
            "current_status": "missing",
            "failure_if_absent": "activation law is only branch-local",
        },
        {
            "requirement": "perturbation_lensing_response",
            "needed_statement": "the same parent memory sector must give metric potentials, sound speed, anisotropic stress, and lensing",
            "current_status": "missing",
            "failure_if_absent": "CMB remains compressed-distance-only and not support-capable",
        },
        {
            "requirement": "local_GR_PPN_silence",
            "needed_statement": "the parent current must vanish or be screened in local systems while remaining cosmologically active",
            "current_status": "missing",
            "failure_if_absent": "unified theory branch fails the GR-reduction standard",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "regularity_selection_derives_p3",
            "status": "pass_partial",
            "reason": "p=3 is the minimal integer endpoint power that gives F(0)=F'(0)=F''(0)=0 and passes the scalar-action repair gate",
            "allowed_claim": "p=3 is regularity-selected",
        },
        {
            "gate": "survival_law_chain_exact",
            "status": "pass_conditional",
            "reason": "if F=1-exp[-I] and I=X^3, then dF/dN=(1-F)3X^2/u3 exactly",
            "allowed_claim": "the equation chain is exact under the stated exposure ansatz",
        },
        {
            "gate": "p3_parent_dynamics_derived",
            "status": "fail",
            "reason": "no parent action or current equation has yet produced I=X_FLRW^3",
            "allowed_claim": "not derived",
        },
        {
            "gate": "u3_parent_predicted",
            "status": "fail",
            "reason": "u3 is inherited from matching the old N50, not predicted",
            "allowed_claim": "transition scale borrowed",
        },
        {
            "gate": "bmem_parent_predicted",
            "status": "fail",
            "reason": "b_mem remains a calibrated closure amplitude",
            "allowed_claim": "amplitude not derived",
        },
        {
            "gate": "conservation_owner_defined",
            "status": "fail",
            "reason": "no covariant exchange/conservation equation owns the memory source",
            "allowed_claim": "Bianchi gate open",
        },
        {
            "gate": "closure_candidate_retained",
            "status": "pass",
            "reason": "the regularized C2 branch remains alive as an internal closure candidate",
            "allowed_claim": "retained as closure candidate only",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "reason": "parent activation, perturbations, official CMB, and local GR link are still missing",
            "allowed_claim": "no support claim",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "parent_activation_law_attempt",
            "status": "p3_activation_law_regularly_selected_not_parent_derived",
            "what_was_earned": "p=3 now has a clean minimal-regularity and double-zero memory-current interpretation",
            "what_failed": "no parent action/current derives X_FLRW, J_M, u3, b_mem, conservation, perturbations, or local silence",
            "next_target": "51-FLRW-memory-current-contract.md",
        },
        {
            "decision": "route_status",
            "status": "closure_candidate_retained_not_promoted",
            "what_was_earned": "the C2 branch is more theoretically disciplined than a fitted fractional onset",
            "what_failed": "it is still not a fundamental field-theory derivation",
            "next_target": "write the exact contract a parent FLRW memory current must satisfy",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Attempt the parent activation law derivation.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    candidate_rows = read_csv("46_candidate_laws")
    c2_law = row_where(candidate_rows, candidate=C2_CANDIDATE)
    statuses = {key: load_json(key) for key in SOURCE_PATHS if key.endswith("_status")}

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-parent-activation-law-attempt"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    equations = activation_equation_rows(c2_law)
    routes = derivation_route_rows()
    contract = parent_contract_rows(c2_law)
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "activation_law_equation_chain.csv", equations, list(equations[0].keys()))
    write_csv(results_dir / "candidate_parent_derivation_routes.csv", routes, list(routes[0].keys()))
    write_csv(results_dir / "parent_contract_requirements.csv", contract, list(contract[0].keys()))
    write_csv(results_dir / "gate_results.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    u3 = float(c2_law["u_s"])
    status = {
        "status": "complete_parent_activation_law_attempt",
        "readout": "p3_activation_law_regularly_selected_not_parent_derived",
        "recommendation": "write_FLRW_memory_current_contract_next",
        "next_target": "51-FLRW-memory-current-contract.md",
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "key_metrics": {
            "candidate": C2_CANDIDATE,
            "u3": u3,
            "N50": float(c2_law["N50"]),
            "endpoint_power": float(c2_law["endpoint_power"]),
            "F_prime_0": 0.0,
            "F_double_prime_0": 0.0,
            "F_triple_prime_0": 6.0 / (u3**3),
            "J_M_0": 0.0,
            "J_M_prime_0": 0.0,
            "C2_delta_late_plus_Hz_vs_original": statuses["47_status"]["best_repair_delta_late_plus_Hz_vs_original"],
            "C2_delta_total_vs_original": statuses["48_status"]["C2_delta_total_vs_original"],
            "missing_parent_contract_requirements": len(contract),
        },
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "activation_law_equation_chain": str(results_dir / "activation_law_equation_chain.csv"),
            "candidate_parent_derivation_routes": str(results_dir / "candidate_parent_derivation_routes.csv"),
            "parent_contract_requirements": str(results_dir / "parent_contract_requirements.csv"),
            "gate_results": str(results_dir / "gate_results.csv"),
            "decision": str(results_dir / "decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(status["readout"] + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
