from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "GR-reduction-derivation-priority-ledger"
STATUS = "GR_connection_and_derivation_priority_reset_no_local_GR_promotion"
CLAIM_CEILING = "programme_orientation_and_proof_queue_only_no_GR_or_PPN_pass_claim"
NEXT_TARGET = "356-parent-action-ward-identity-and-projector-variation.md"


SOURCE_DOCS = [
    {
        "path": "346-GR-and-derivation-north-star-spine.md",
        "role": "sets the project north star: connect to GR and derive closures",
    },
    {
        "path": "347-local-GR-parent-reduction-theorem-attempt.md",
        "role": "conditional local-GR reduction theorem and N-gate blockers",
    },
    {
        "path": "348-N5-projector-stress-conservation-theorem.md",
        "role": "conditional projector-stress conservation/local bulk silence route",
    },
    {
        "path": "349-parent-PD-FLRW-projection-compatibility-gate.md",
        "role": "tests whether the same parent projector can support local and FLRW branches",
    },
    {
        "path": "350-parent-PD-ownership-and-cell-state-derivation-gate.md",
        "role": "parent ownership and cell-state derivation status for amplitude closures",
    },
    {
        "path": "351-local-GR-spin2-rank2-bridge-or-boundary-PPN-gate.md",
        "role": "rejects spin-2 counting as rank-2 amplitude derivation; keeps boundary/PPN route",
    },
    {
        "path": "352-boundary-nohair-and-PPN-residual-vector-gate.md",
        "role": "boundary residual decomposition and symbolic PPN residual owners",
    },
    {
        "path": "353-boundary-nohair-theorem-attempt-or-PPN-bound-runner.md",
        "role": "no-hair theorem contract and first proxy local-bound runner",
    },
    {
        "path": "354-official-local-bound-source-lock-or-nohair-proof-deepening.md",
        "role": "source-locks local target scales and deepens no-hair proof obligations",
    },
]


GR_REDUCTION_CHAIN = [
    {
        "order": 1,
        "layer": "parent variational action",
        "GR_connection_target": "write S_parent[g/e, X, projectors, boundary data, matter]",
        "current_status": "contract fragments exist",
        "derived_status": "not_derived",
        "main_blocker": "full parent field content and allowed variations not fixed",
        "proof_obligation": "state the dynamical fields, gauge redundancies, boundary variables, and variation rules",
        "why_it_matters": "GR cannot be derived from a parent action that has not been made variationally explicit",
    },
    {
        "order": 2,
        "layer": "single physical geometry",
        "GR_connection_target": "derive one metric/coframe seen by matter, clocks, rulers, and lensing",
        "current_status": "specified as N0 contract",
        "derived_status": "not_derived",
        "main_blocker": "universal matter coupling is an assumption, not a theorem",
        "proof_obligation": "show matter couples minimally to the same g/e and carries no independent MTS charge",
        "why_it_matters": "without one geometry the local limit becomes a generic metric/nonmetric modified gravity branch",
    },
    {
        "order": 3,
        "layer": "Ward/Bianchi identity",
        "GR_connection_target": "derive nabla_mu(T_matter^munu + kappa^-1 E_MTS^munu)=0",
        "current_status": "conditional ledger written",
        "derived_status": "conditional",
        "main_blocker": "projector/boundary variation is not fully owned",
        "proof_obligation": "vary the full parent action under diffeomorphisms, including projector and boundary terms",
        "why_it_matters": "dropping hidden stress breaks conservation and fakes the GR reduction",
    },
    {
        "order": 4,
        "layer": "local no-hair/silence",
        "GR_connection_target": "prove E_MTS_munu has no local bulk exterior support",
        "current_status": "no-hair contract and partial boundary route",
        "derived_status": "open_conditional",
        "main_blocker": "double-zero/local suppression mechanism not parent-derived",
        "proof_obligation": "prove auxiliary gradients, projector stress, and memory/load residuals vanish or are boundary-only",
        "why_it_matters": "any remaining bulk scalar/vector/tensor hair produces PPN, WEP, clock, or fifth-force residuals",
    },
    {
        "order": 5,
        "layer": "Einstein-Hilbert exterior",
        "GR_connection_target": "reduce the local exterior equations to G_munu + Lambda g_munu = kappa T_munu",
        "current_status": "conditional theorem",
        "derived_status": "not_promoted",
        "main_blocker": "metric-only exterior and vanishing E_MTS are not derived",
        "proof_obligation": "show the surviving local metric operator is the EH operator plus Lambda under the stated assumptions",
        "why_it_matters": "this is the actual MTS to GR bridge",
    },
    {
        "order": 6,
        "layer": "Newtonian limit",
        "GR_connection_target": "recover Poisson/Newton with a fixed measured G",
        "current_status": "follows conditionally from EH plus universal coupling",
        "derived_status": "conditional",
        "main_blocker": "G normalization and local silence remain upstream",
        "proof_obligation": "derive weak-field limit, Poisson equation, and normalization of kappa",
        "why_it_matters": "GR must reduce to Newton, so MTS must inherit that chain without new local forces",
    },
    {
        "order": 7,
        "layer": "PPN residual vector",
        "GR_connection_target": "compute gamma-1, beta-1, alpha_i, clock, WEP, fifth-force residuals from E_MTS",
        "current_status": "symbolic owner map plus source-locked target scales",
        "derived_status": "not_calculated",
        "main_blocker": "closed residual coefficients not derived",
        "proof_obligation": "linearize/quadratic-expand the local equations and map each residual to source-locked targets",
        "why_it_matters": "this is the local experimental guardrail, not the proof itself",
    },
    {
        "order": 8,
        "layer": "cosmology/FLRW compatibility",
        "GR_connection_target": "show local GR silence and global FLRW memory are projections of the same parent structure",
        "current_status": "compatibility route exists but amplitude closures remain",
        "derived_status": "partial",
        "main_blocker": "B_mem, q_trace, epsilon_H, H_star/H0 remain closure or conditional",
        "proof_obligation": "derive the projection weights and calibration identities from parent symmetries or dynamics",
        "why_it_matters": "a unified theory cannot use unrelated local and cosmological mechanisms",
    },
]


DERIVATION_DEBTS = [
    {
        "object": "N0 unique metric/coframe",
        "current_label": "contract",
        "desired_label": "theorem",
        "proof_route": "universal matter coupling from parent gauge/observer structure",
        "promotion_blocked_until": "same geometry controls matter, clocks, rulers, lensing, and PPN",
    },
    {
        "object": "N5 projector stress",
        "current_label": "hard blocker partly sharpened",
        "desired_label": "zero/boundary/conserved theorem",
        "proof_route": "metric-independent projector or full retained stress variation with Ward identity",
        "promotion_blocked_until": "T_projector is not silently dropped",
    },
    {
        "object": "N6 metric-only EH exterior",
        "current_label": "conditional",
        "desired_label": "local GR theorem",
        "proof_route": "prove all nonmetric local exterior fields are absent or pure gauge, then identify EH operator",
        "promotion_blocked_until": "E_MTS_munu is zero/boundary-only through PPN order",
    },
    {
        "object": "local no-hair double zero",
        "current_label": "contract",
        "desired_label": "mechanism",
        "proof_route": "derive stationary local extremum and suppression length from parent equations",
        "promotion_blocked_until": "local gradients and amplitudes are bounded without plateau axiom",
    },
    {
        "object": "PPN residual vector",
        "current_label": "owner map",
        "desired_label": "computed coefficients",
        "proof_route": "weak-field expansion of the parent-owned local equations",
        "promotion_blocked_until": "gamma, beta, preferred-frame, clock, WEP, and fifth-force residuals are numerically bounded",
    },
    {
        "object": "B_mem = 2/27",
        "current_label": "locked closure",
        "desired_label": "parent-derived amplitude or honest permanent closure",
        "proof_route": "derive dim 27, active rank 2, and normalization from parent state space",
        "promotion_blocked_until": "rank/dimension are not inserted after the fact",
    },
    {
        "object": "epsilon_H = 1",
        "current_label": "closure/conditional exact-readout target",
        "desired_label": "Ward/Hamiltonian normalization theorem",
        "proof_route": "derive normalization from variation, conserved charge, or observer Hamiltonian",
        "promotion_blocked_until": "the unit value is not chosen by calibration convenience",
    },
    {
        "object": "H_star = H0",
        "current_label": "identity route but not parent selection",
        "desired_label": "boundary/observer selection theorem",
        "proof_route": "derive why the present Hubble scale is the parent reference scale",
        "promotion_blocked_until": "the scale is selected dynamically rather than fitted",
    },
    {
        "object": "FLRW memory projection",
        "current_label": "partial compatibility",
        "desired_label": "derived projection law",
        "proof_route": "derive the FLRW memory source and projection weights from the same P_D used locally",
        "promotion_blocked_until": "global memory and local silence share one parent mechanism",
    },
    {
        "object": "perturbation/CMB owner",
        "current_label": "open",
        "desired_label": "Boltzmann-level interface",
        "proof_route": "derive mu(a,k), slip, sound speed, source terms, and initial-condition behavior",
        "promotion_blocked_until": "compressed-distance success is connected to perturbation consistency",
    },
]


NO_CHEAT_RULES = [
    {
        "rule": "do_not_assume_GR_limit",
        "meaning": "the local Einstein equations must emerge from the parent action, not be appended as a background",
    },
    {
        "rule": "do_not_drop_projector_stress",
        "meaning": "projector/boundary stress must be zero, boundary-only, or retained in a conserved ledger",
    },
    {
        "rule": "do_not_use_PPN_runner_as_proof",
        "meaning": "source-locked local bounds are guardrails after equations exist, not a derivation of those equations",
    },
    {
        "rule": "do_not_promote_closure_constants",
        "meaning": "B_mem, epsilon_H, H_star/H0, u3, dim 27, and rank 2 remain closure/conditional until parent-derived",
    },
    {
        "rule": "do_not_let_cosmology_bypass_GR",
        "meaning": "late-time fits can keep a branch alive but cannot substitute for local GR reduction",
    },
    {
        "rule": "do_not_demand_knockout_only",
        "meaning": "empirical ties or slight wins matter if MTS pays the theory bill with a coherent field-theory derivation",
    },
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": "parent Ward identity with projector variation",
        "deliverable": NEXT_TARGET,
        "pass_condition": "all metric, projector, domain, and boundary variations appear in the conservation identity",
        "failure_meaning": "local GR route stays conditional because hidden stress may remain",
    },
    {
        "priority": 2,
        "target": "local no-hair/silence theorem",
        "deliverable": "prove or bound E_MTS_munu -> 0 in local exterior",
        "pass_condition": "auxiliary fields are pure gauge, boundary-only, or source-locked below PPN/WEP/clock bounds",
        "failure_meaning": "local branch becomes explicit modified-gravity closure rather than GR derivation",
    },
    {
        "priority": 3,
        "target": "EH exterior operator derivation",
        "deliverable": "metric-only local action and weak-field operator map",
        "pass_condition": "surviving operator is EH plus Lambda with no extra local propagating modes",
        "failure_meaning": "MTS does not yet connect to GR at the equation level",
    },
    {
        "priority": 4,
        "target": "source-locked local PPN runner",
        "deliverable": "local bound runner using 354 source-locked scales and quarantined open sectors",
        "pass_condition": "computed residual vector is below locked target scales or explicitly fails",
        "failure_meaning": "derive stronger silence or demote local branch",
    },
    {
        "priority": 5,
        "target": "closure-to-theorem conversion",
        "deliverable": "rank/dim/amplitude/calibration derivation attempts after local GR spine is stable",
        "pass_condition": "at least one closure value is derived from parent structure without post-hoc insertion",
        "failure_meaning": "keep closure labels honest while continuing empirical tests",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for doc in SOURCE_DOCS:
        source_path = ROOT / doc["path"]
        rows.append(
            {
                "source_file": doc["path"],
                "exists": source_path.exists(),
                "role": doc["role"],
            }
        )
    return rows


def gate_result_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = [row["source_file"] for row in source_rows if not row["exists"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing else "fail",
            "evidence": "all cited checkpoint files exist" if not missing else "; ".join(missing),
        },
        {
            "gate": "GR_connection_priority_explicit",
            "status": "pass",
            "evidence": "GR reduction chain is ordered from parent action to local PPN guardrails",
        },
        {
            "gate": "derivation_debt_explicit",
            "status": "pass",
            "evidence": f"{len(DERIVATION_DEBTS)} closure/open objects mapped to proof routes",
        },
        {
            "gate": "no_GR_promotion",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
        {
            "gate": "local_bound_runner_deprioritized_as_proof",
            "status": "pass",
            "evidence": "runner is retained as guardrail after parent Ward/no-hair equations, not treated as derivation",
        },
        {
            "gate": "next_derivation_target_selected",
            "status": "pass",
            "evidence": NEXT_TARGET,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "local_GR_promoted": False,
            "PPN_pass_claimed": False,
            "main_direction": "connect_MTS_to_GR_and_replace_closures_with_derivations",
            "next_target": NEXT_TARGET,
            "rationale": "the source-locked local runner is useful, but the decisive route is parent Ward identity, projector variation, local no-hair, EH exterior, then PPN residuals",
        }
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    run_dir = ROOT / "runs" / f"{args.timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    gates = gate_result_rows(source_rows)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": source_rows,
        "GR_reduction_chain.csv": GR_REDUCTION_CHAIN,
        "derivation_debt_ledger.csv": DERIVATION_DEBTS,
        "no_cheat_rules.csv": NO_CHEAT_RULES,
        "next_derivation_queue.csv": NEXT_QUEUE,
        "gate_results.csv": gates,
        "decision.csv": decisions,
    }
    for name, rows in outputs.items():
        write_csv(results_dir / name, rows)

    status = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "generated": sorted(outputs),
        "source_paths_missing": sum(1 for row in source_rows if not row["exists"]),
        "derivation_debts_mapped": len(DERIVATION_DEBTS),
        "GR_reduction_layers_mapped": len(GR_REDUCTION_CHAIN),
        "local_GR_promoted": False,
        "PPN_pass_claimed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text("done\n", encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
