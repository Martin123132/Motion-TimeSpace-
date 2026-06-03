#!/usr/bin/env python3
"""Define the parent memory/action owner contract for the quarter-locked branch."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "19_parent_action_skeleton": Path("19-constrained-parent-action-skeleton.md"),
    "51_memory_current_doc": Path("51-FLRW-memory-current-contract.md"),
    "53_projection_doc": Path("53-coherent-projection-local-silence-gate.md"),
    "55_quarter_smoke_doc": Path("55-u3-quarter-lock-smoke.md"),
    "56_cell_theorem_doc": Path("56-u3-quarter-parent-cell-theorem-attempt.md"),
    "56_status": Path("runs/20260531-104327-u3-quarter-parent-cell-theorem-attempt/status.json"),
    "56_gates": Path("runs/20260531-104327-u3-quarter-parent-cell-theorem-attempt/results/gate_results.csv"),
    "55_status": Path("runs/20260531-104003-u3-quarter-lock-smoke/status.json"),
}


def absolute_source(key: str) -> Path:
    return POST_CHECKPOINT / SOURCE_PATHS[key]


def load_json(key: str) -> dict[str, Any]:
    return json.loads(absolute_source(key).read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


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


def owner_field_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "e^A_mu",
            "role": "observer coframe and metric carrier",
            "must_own": "3+1 coherent observer cell C4",
            "current_status": "available_in_skeleton",
            "failure_if_missing": "u3=1/4 cell normalization floats free",
        },
        {
            "object": "u^mu or clock-flow field",
            "role": "time-flow congruence defining expansion tensor",
            "must_own": "Theta^i_j and the clock/coherence leg",
            "current_status": "missing_parent_origin",
            "failure_if_missing": "Q_coh and <theta>_D depend on an assumed flow",
        },
        {
            "object": "D or chi_D",
            "role": "coherent-domain selector or window field",
            "must_own": "maximal coherent volume-flow domain and bound-domain silence",
            "current_status": "contract_only",
            "failure_if_missing": "local silence remains a smoothing rule",
        },
        {
            "object": "Q_coh^i_j",
            "role": "coherent accumulated spatial load tensor",
            "must_own": "spatial determinant exposure p=3",
            "current_status": "kinematic_candidate",
            "failure_if_missing": "activation shape is not field-theoretic",
        },
        {
            "object": "C4",
            "role": "3+1 coherent cell normalization",
            "must_own": "u3=1/4 and X_FLRW=4N",
            "current_status": "conditional_candidate",
            "failure_if_missing": "quarter lock remains numerically cute",
        },
        {
            "object": "I_M",
            "role": "cumulative memory exposure",
            "must_own": "I_M=det(Q_coh) and F=1-exp(-I_M)",
            "current_status": "conditional_survival_form",
            "failure_if_missing": "memory activation is closure language",
        },
        {
            "object": "T^mu_nu_M or E^mu_nu_M",
            "role": "memory stress/geometric owner",
            "must_own": "b_mem, conservation, background pressure/exchange, perturbations",
            "current_status": "missing",
            "failure_if_missing": "no Bianchi-safe cosmology or CMB support",
        },
        {
            "object": "lambda_M or constraint/current multiplier",
            "role": "enforces or sources memory-cell current",
            "must_own": "why spatial determinant and 3+1 normalization are selected",
            "current_status": "missing",
            "failure_if_missing": "the branch remains a list of contracts",
        },
    ]


def action_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "term": "S_geom[e]",
            "required_variation": "metric/coframe equation with Bianchi identity",
            "owns": "gravitational/coframe backbone",
            "status": "skeleton_only",
            "no_smuggling_rule": "must not import GR equations as hidden proof",
        },
        {
            "term": "S_flow[e,u,lambda_u]",
            "required_variation": "defines physical clock-flow congruence u^mu",
            "owns": "Theta^i_j and the time leg of C4",
            "status": "missing",
            "no_smuggling_rule": "u^mu cannot be chosen separately for FLRW and local systems",
        },
        {
            "term": "S_domain[u,chi_D]",
            "required_variation": "defines coherent domain/window from volume-flow extremality or constraint",
            "owns": "D and local bound-domain silence",
            "status": "missing",
            "no_smuggling_rule": "domain cannot be tuned to local tests",
        },
        {
            "term": "S_Q[Q,u,chi_D]",
            "required_variation": "sets Q_coh^i_j=(1/u3) integral P_coh[Theta]^i_j d tau or equivalent local current",
            "owns": "coherent accumulated spatial load",
            "status": "contract_only",
            "no_smuggling_rule": "Q cannot be defined by demanding det(Q)=(4N)^3",
        },
        {
            "term": "S_cell[e,u,Q,lambda_cell]",
            "required_variation": "selects 3+1 normalization X_FLRW=4N and spatial determinant exposure",
            "owns": "u3=1/4 and p=3 split",
            "status": "central_missing_owner",
            "no_smuggling_rule": "must explain why normalization is 4D but exposure determinant is spatial 3D",
        },
        {
            "term": "S_memory[I_M,F,lambda_M]",
            "required_variation": "gives saturating exposure law dF=(1-F)dI_M or justified replacement",
            "owns": "activation map F=1-exp(-I_M)",
            "status": "conditional",
            "no_smuggling_rule": "survival law cannot be imported solely because it fits",
        },
        {
            "term": "S_stress[M,e]",
            "required_variation": "produces memory energy density, pressure, anisotropic stress, sound speed, and exchange",
            "owns": "b_mem, Bianchi bookkeeping, perturbations, lensing",
            "status": "missing",
            "no_smuggling_rule": "cannot borrow quintessence/GR perturbations as proof",
        },
    ]


def equation_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "target": "p=3",
            "required_equation": "I_M=det(Q_coh), Q_coh^i_j=X_FLRW delta^i_j in FLRW",
            "owner_needed": "S_cell or S_Q",
            "current_status": "conditional_pass",
            "missing_piece": "action reason for determinant exposure",
        },
        {
            "target": "u3=1/4",
            "required_equation": "d ln C4/dtau=4H -> X_FLRW=4N=N/u3",
            "owner_needed": "S_cell",
            "current_status": "conditional_pass",
            "missing_piece": "parent reason for clock leg and 3+1 normalization",
        },
        {
            "target": "domain D",
            "required_equation": "D extremizes coherent volume-flow or satisfies parent boundary condition",
            "owner_needed": "S_domain",
            "current_status": "contract_only",
            "missing_piece": "non-fitted bound/unbound domain theorem",
        },
        {
            "target": "local silence",
            "required_equation": "dV_D/dtau=0 -> Q_coh=0 -> I_M=0 for stationary bound domains",
            "owner_needed": "S_domain plus S_Q",
            "current_status": "pass_conditional",
            "missing_piece": "dynamic local/radiative safety",
        },
        {
            "target": "b_mem",
            "required_equation": "rho_M or geometric memory contribution amplitude from S_stress variation",
            "owner_needed": "S_stress",
            "current_status": "missing",
            "missing_piece": "amplitude theorem",
        },
        {
            "target": "Bianchi conservation",
            "required_equation": "nabla_mu(G_eff^mu_nu - T_m^mu_nu - T_M^mu_nu)=0 or explicit exchange Q^nu",
            "owner_needed": "S_geom plus S_stress",
            "current_status": "missing",
            "missing_piece": "covariant owner of memory exchange",
        },
        {
            "target": "perturbation/lensing response",
            "required_equation": "delta T_M, c_s^2, pi_M, Phi/Psi response from same owner",
            "owner_needed": "S_stress",
            "current_status": "missing",
            "missing_piece": "official CMB-capable perturbation equations",
        },
    ]


def risk_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "risk": "split_owner_problem",
            "severity": "high",
            "description": "p=3, u3=1/4, D, and b_mem may remain separate plausible stories",
            "mitigation": "require S_cell/S_stress to own all of them or demote to closure-only",
        },
        {
            "risk": "4D_vs_3D_inconsistency",
            "severity": "high",
            "description": "normalization uses 3+1 cell while exposure uses 3D determinant",
            "mitigation": "derive normalization from observer cell and exposure from spatial memory flux in one action",
        },
        {
            "risk": "domain_rescue_knob",
            "severity": "high",
            "description": "D could be chosen to avoid local tests",
            "mitigation": "derive D from volume-flow extremality/boundary condition before more local claims",
        },
        {
            "risk": "amplitude_free_parameter",
            "severity": "high",
            "description": "b_mem can keep the branch phenomenological even if shape/scale improve",
            "mitigation": "make amplitude theorem the next empirical-promotion gate after action owner",
        },
        {
            "risk": "CMB_support_import",
            "severity": "high",
            "description": "compressed distance success can tempt borrowed perturbations",
            "mitigation": "forbid official CMB support claims until perturbation/lensing owner exists",
        },
        {
            "risk": "local_GR_not_unified",
            "severity": "medium",
            "description": "local observer-cell reciprocity and cosmology memory-cell normalization may remain disconnected",
            "mitigation": "require same coframe/cell current to underwrite both branches",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "single_owner_contract_written",
            "status": "pass",
            "detail": "minimal S_flow/S_domain/S_Q/S_cell/S_memory/S_stress ownership contract is explicit",
        },
        {
            "gate": "p3_and_u3_owned_by_same_sector",
            "status": "pass_conditional",
            "detail": "S_cell can own spatial determinant p=3 and 3+1 normalization u3=1/4 if derived",
        },
        {
            "gate": "owner_action_derived",
            "status": "fail",
            "detail": "the contract names required terms but does not derive equations from an action",
        },
        {
            "gate": "domain_D_parent_derived",
            "status": "fail",
            "detail": "D remains a coherent-volume contract without variational boundary rule",
        },
        {
            "gate": "bmem_amplitude_derived",
            "status": "fail",
            "detail": "no memory stress amplitude theorem yet",
        },
        {
            "gate": "Bianchi_conservation_owner_defined",
            "status": "fail",
            "detail": "covariant exchange/geometric owner not yet specified",
        },
        {
            "gate": "perturbation_lensing_owner_defined",
            "status": "fail",
            "detail": "sound speed, anisotropic stress, and metric-potential response still missing",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "contract sharpens the missing parent theory; it is not evidence",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "memory_action_owner_status",
            "status": "contract_written_not_satisfied",
            "evidence": "one owner contract now names required fields, terms, equations, and risks",
            "next_action": "attempt minimal S_cell variation or demote cell route to explicit closure",
        },
        {
            "decision": "quarter_branch_status",
            "status": "retained_less_free_closure_candidate_pending_owner",
            "evidence": "u3=1/4 survived smoke and has a conditional cell route, but no action owner",
            "next_action": "derive S_cell or mark quarter lock as closure-only",
        },
        {
            "decision": "recommended_next_target",
            "status": "58-S-cell-variation-attempt.md",
            "evidence": "S_cell is the central bottleneck for p=3/u3=1/4 split",
            "next_action": "try the minimal variational mechanism for spatial determinant plus 3+1 normalization",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Memory action-owner contract.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    status_56 = load_json("56_status")
    status_55 = load_json("55_status")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-memory-action-owner-contract"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    fields = owner_field_rows()
    actions = action_contract_rows()
    equations = equation_contract_rows()
    risks = risk_register_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "owner_field_contract.csv", fields, list(fields[0].keys()))
    write_csv(results_dir / "action_term_contract.csv", actions, list(actions[0].keys()))
    write_csv(results_dir / "equation_ownership_contract.csv", equations, list(equations[0].keys()))
    write_csv(results_dir / "risk_register.csv", risks, list(risks[0].keys()))
    write_csv(results_dir / "gate_results.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    status = {
        "status": "complete_memory_action_owner_contract",
        "readout": "memory_action_owner_contract_written_not_satisfied",
        "recommendation": "attempt_S_cell_variation_next",
        "next_target": "58-S-cell-variation-attempt.md",
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "central_missing_owner": "S_cell[e,u,Q,lambda_cell] plus S_stress[M,e]",
        "key_metrics": {
            "u3_quarter": status_56["key_metrics"]["u3_quarter"],
            "quarter_delta_total_vs_fitted_C2": status_55["key_metrics"]["quarter_delta_total_vs_fitted_C2"],
            "owner_fields": len(fields),
            "action_terms": len(actions),
            "equation_targets": len(equations),
            "high_severity_risks": sum(1 for row in risks if row["severity"] == "high"),
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
        },
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "owner_field_contract": str(results_dir / "owner_field_contract.csv"),
            "action_term_contract": str(results_dir / "action_term_contract.csv"),
            "equation_ownership_contract": str(results_dir / "equation_ownership_contract.csv"),
            "risk_register": str(results_dir / "risk_register.csv"),
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
