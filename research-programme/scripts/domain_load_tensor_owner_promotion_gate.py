#!/usr/bin/env python3
"""Promotion gate for the coherent-domain and load-tensor owner."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
CONTRACT_RUN = RUNS_ROOT / "20260531-210000-consolidated-locked-memory-branch-contract"
CONTRACT_RESULTS = CONTRACT_RUN / "results"

CLAIM_CEILING = "domain_load_owner_contract_sharpened_not_parent_derived"


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def source_register_rows(script_path: Path, contract_run: Path) -> list[dict[str, Any]]:
    contract_results = contract_run / "results"
    paths = [
        script_path,
        WORK_DIR / "52-load-tensor-origin-attempt.md",
        WORK_DIR / "53-coherent-projection-local-silence-gate.md",
        WORK_DIR / "54-coherent-domain-and-u3-origin.md",
        WORK_DIR / "138-coherent-volume-pressure-kernel-theorem.md",
        WORK_DIR / "141-consolidated-locked-memory-branch-contract.md",
        contract_run / "status.json",
        contract_results / "branch_equation_contract.csv",
        contract_results / "promotion_requirements.csv",
        contract_results / "claim_control_ledger.csv",
        contract_results / "decision.csv",
    ]
    return [
        {
            "source": path.name,
            "path": str(path),
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path in paths
    ]


def domain_selector_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "external_smoothing_domain",
            "definition": "choose a fixed averaging scale or hand-selected region",
            "FLRW": "works",
            "local_silence": "can_be_tuned",
            "noncircularity": "fail",
            "verdict": "rejected_rescue_knob",
        },
        {
            "candidate": "pointwise_no_domain",
            "definition": "use local theta or full Theta^i_j directly",
            "FLRW": "works",
            "local_silence": "fail_risk",
            "noncircularity": "partial",
            "verdict": "rejected_local_hair_risk",
        },
        {
            "candidate": "maximal_coherent_volume_flow_domain",
            "definition": "largest connected domain with stable sign of <theta>_D and small normalized expansion variance",
            "FLRW": "pass",
            "local_silence": "pass_conditional_for_bound_volume_stable_systems",
            "noncircularity": "partial",
            "verdict": "best_contract_not_parent_action",
        },
        {
            "candidate": "variational_phase_field_domain",
            "definition": "chi_D extremizes a coherence functional with boundary cost and expansion-variance cost",
            "FLRW": "pass_conditional",
            "local_silence": "pass_conditional",
            "noncircularity": "open",
            "verdict": "best_parent_action_route_if_coefficients_are_fixed",
        },
        {
            "candidate": "relative_boundary_current_domain",
            "definition": "D is selected by closed relative current J_rel=(j3,b2) and trivial/nontrivial cohomology class",
            "FLRW": "pass_contract",
            "local_silence": "pass_conditional_if_local_class_trivial",
            "noncircularity": "open",
            "verdict": "best_topological_support_not_full_selector",
        },
    ]


def load_tensor_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "flow_congruence",
            "equation": "Theta^i_j = h^{i alpha} h_{j beta} nabla_alpha u^beta",
            "status": "kinematic_available",
            "meaning": "spatial expansion/load tensor exists before FLRW",
            "blocker": "u^mu parent clock-flow owner still must be fixed",
        },
        {
            "step": "coherent_projection",
            "equation": "P_coh[Theta]^i_j = (1/3)<theta>_D delta^i_j",
            "status": "conditional_projection",
            "meaning": "memory channel responds to coherent volume growth, not local shear",
            "blocker": "domain D must be parent-selected",
        },
        {
            "step": "volume_time",
            "equation": "N_D=(1/3)ln(V_D0/V_D)",
            "status": "conditional_owner",
            "meaning": "turns the accumulated trace into a scalar coherent-volume load",
            "blocker": "boundary variation and reference volume must be derived",
        },
        {
            "step": "load_tensor",
            "equation": "Q_coh^i_j = (N_D/u3) delta^i_j",
            "status": "owned_if_ND_and_u3_owned",
            "meaning": "Q is not independent once coherent-volume load is accepted",
            "blocker": "u3=1/4 and D remain conditional",
        },
        {
            "step": "activation_exposure",
            "equation": "I_M=det(Q_coh)=(N_D/u3)^3",
            "status": "pass_conditional",
            "meaning": "cubic exposure follows from determinant of isotropic coherent load",
            "blocker": "determinant coupling still needs parent stress/action owner",
        },
    ]


def branch_limit_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "FLRW",
            "input_condition": "V_D proportional to a^3, <theta>_D=3H",
            "Q_result": "Q_coh^i_j=(N/u3)delta^i_j",
            "memory_result": "I_M=(N/u3)^3",
            "status": "pass_conditional",
            "remaining_risk": "requires D to be homogeneous coherent domain",
        },
        {
            "branch": "Minkowski_local",
            "input_condition": "dV_D/dtau=0",
            "Q_result": "Q_coh=0",
            "memory_result": "I_M=0",
            "status": "pass_conditional",
            "remaining_risk": "requires correct local domain selection",
        },
        {
            "branch": "stationary_solar_system",
            "input_condition": "bound physical volume stable",
            "Q_result": "Q_coh approximately 0",
            "memory_result": "local memory off",
            "status": "pass_conditional",
            "remaining_risk": "needs PPN proof and boundary terms",
        },
        {
            "branch": "tracefree_shear_or_GW",
            "input_condition": "theta trace vanishes at leading order",
            "Q_result": "coherent trace channel off",
            "memory_result": "no first-order determinant activation",
            "status": "pass_conditional",
            "remaining_risk": "second-order/boundary effects not derived",
        },
        {
            "branch": "virialized_galaxy",
            "input_condition": "time-averaged coherent volume stable",
            "Q_result": "Q_coh approximately 0",
            "memory_result": "local memory suppressed",
            "status": "open_conditional",
            "remaining_risk": "bound/unbound split may import GR/Newtonian assumptions",
        },
        {
            "branch": "collapse_or_merger",
            "input_condition": "coherent local volume changes",
            "Q_result": "Q_coh nonzero possible",
            "memory_result": "potential local activation",
            "status": "open_risk",
            "remaining_risk": "could source local/transient deviations unless action suppresses or confines it",
        },
    ]


def phase_field_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "term": "binary_domain_constraint",
            "sketch": "lambda_chi chi_D(1-chi_D)",
            "purpose": "force a sharp or auxiliary domain selector",
            "status": "formal",
            "risk": "can become hand-imposed boundary",
        },
        {
            "term": "coherence_variance",
            "sketch": "chi_D (theta-<theta>_D)^2 / (<theta>_D^2+epsilon)",
            "purpose": "select domains with coherent volume flow",
            "status": "candidate",
            "risk": "epsilon/normalization must not become tuning knob",
        },
        {
            "term": "boundary_cost",
            "sketch": "kappa |nabla chi_D|^2 or relative-current closure",
            "purpose": "avoid ragged domains and wall stress",
            "status": "candidate",
            "risk": "kappa must be fixed or topological, not fitted",
        },
        {
            "term": "maximality_rule",
            "sketch": "choose largest connected stable-sign domain after coherence constraints",
            "purpose": "prevent tiny domains chosen to dodge local tests",
            "status": "contract",
            "risk": "global optimization must be covariant/causal",
        },
        {
            "term": "relative_boundary_current",
            "sketch": "d_rel J_rel=0 with local trivial class and FLRW nontrivial class",
            "purpose": "carry boundary exchange without physical wall stress",
            "status": "support_contract",
            "risk": "representative not parent-selected",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "Q_defined_before_FLRW",
            "status": "pass_conditional",
            "evidence": "Theta^i_j and coherent trace projection define Q before imposing FLRW",
        },
        {
            "gate": "Q_independent_blocker_reduced",
            "status": "pass_partial",
            "evidence": "if N_D and u3 are owned, Q_coh=(N_D/u3)delta follows",
        },
        {
            "gate": "domain_parent_selector",
            "status": "fail",
            "evidence": "D is still a maximal coherent-flow contract, not a derived Euler equation",
        },
        {
            "gate": "u3_parent_owner",
            "status": "fail",
            "evidence": "u3=1/4 remains conditional 3+1 cell route, not parent action theorem",
        },
        {
            "gate": "local_stationary_silence",
            "status": "pass_conditional",
            "evidence": "stable volume gives N_D=0 and Q=0",
        },
        {
            "gate": "dynamic_local_safety",
            "status": "open_risk",
            "evidence": "collapse/merger/local boundary motion can activate Q unless action controls it",
        },
        {
            "gate": "promotion_to_parent_field_theory",
            "status": "fail",
            "evidence": "domain, u3, boundary current, and stress action are still conditional/open",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": "domain_load_owner_sharpened_Q_reduced_D_not_derived",
            "evidence": "Q can be owned by coherent-volume load if D and u3 are derived; D remains the main blocker",
        },
        {
            "item": "best_route",
            "verdict": "variational_phase_field_or_relative_boundary_selector",
            "evidence": "future parent work should derive D from a zero-knob coherence/boundary action",
        },
        {
            "item": "local_GR_status",
            "verdict": "stationary_silence_conditional_dynamic_safety_open",
            "evidence": "stable local volumes are safe conditionally; collapse/merger/boundary motion are unresolved",
        },
        {
            "item": "next_target",
            "verdict": "derive_or_demote_domain_selector",
            "evidence": "without parent-selected D, the memory branch remains empirical EFT closure with conditional mechanics",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None = None, contract_run: Path = CONTRACT_RUN) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-domain-load-tensor-owner-promotion-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve(), contract_run)
    missing = [row["path"] for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    contract_status = read_json(contract_run / "status.json")
    promotion_requirements = read_csv_rows(contract_run / "results" / "promotion_requirements.csv")

    domain_candidates = domain_selector_candidate_rows()
    load_owner = load_tensor_owner_rows()
    branch_tests = branch_limit_test_rows()
    phase_field = phase_field_action_rows()
    gates = promotion_gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(results_dir / "domain_selector_candidates.csv", domain_candidates, ["candidate", "definition", "FLRW", "local_silence", "noncircularity", "verdict"])
    write_csv(results_dir / "load_tensor_owner_chain.csv", load_owner, ["step", "equation", "status", "meaning", "blocker"])
    write_csv(results_dir / "branch_limit_tests.csv", branch_tests, ["branch", "input_condition", "Q_result", "memory_result", "status", "remaining_risk"])
    write_csv(results_dir / "phase_field_action_contract.csv", phase_field, ["term", "sketch", "purpose", "status", "risk"])
    write_csv(results_dir / "input_promotion_requirements.csv", promotion_requirements, ["requirement", "must_prove", "current_status", "promotion_gate"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "input_status": contract_status["status"],
        "generated": [
            "source_register.csv",
            "domain_selector_candidates.csv",
            "load_tensor_owner_chain.csv",
            "branch_limit_tests.csv",
            "phase_field_action_contract.csv",
            "input_promotion_requirements.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "derive_or_demote_domain_selector_variational_action",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--contract-run", type=Path, default=CONTRACT_RUN)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_audit(args.output_root, args.timestamp, args.contract_run))


if __name__ == "__main__":
    main()
