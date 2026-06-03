from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "parent-action-ward-identity-and-projector-variation"
STATUS = "parent_Ward_identity_with_projector_force_ledger_written_no_local_GR_promotion"
CLAIM_CEILING = "structural_Ward_identity_contract_only_no_EH_exterior_no_PPN_pass_no_nohair_claim"
NEXT_TARGET = "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md"


SOURCE_DOCS = [
    {
        "path": "347-local-GR-parent-reduction-theorem-attempt.md",
        "role": "conditional GR-reduction theorem and Bianchi burden",
    },
    {
        "path": "348-N5-projector-stress-conservation-theorem.md",
        "role": "metric-independent projector condition for no bulk projector stress",
    },
    {
        "path": "352-boundary-nohair-and-PPN-residual-vector-gate.md",
        "role": "boundary residual decomposition and symbolic PPN owners",
    },
    {
        "path": "353-boundary-nohair-theorem-attempt-or-PPN-bound-runner.md",
        "role": "A1-A7 no-hair contract and proxy residual amplitude scaffold",
    },
    {
        "path": "354-official-local-bound-source-lock-or-nohair-proof-deepening.md",
        "role": "source-locked local target scales and quarantined open bound sectors",
    },
    {
        "path": "355-GR-reduction-and-derivation-priority-ledger.md",
        "role": "sets the parent Ward identity as the next proof target",
    },
    {
        "path": "scripts/domain_projector_action_and_Bianchi_identity.py",
        "role": "earlier domain-projector/Bianchi scaffolding",
    },
    {
        "path": "scripts/GK_parent_metric_Ward_identity_attempt.py",
        "role": "earlier Ward identity attempt for metric/normalization route",
    },
    {
        "path": "scripts/N5_projector_stress_conservation_theorem.py",
        "role": "machine source for checkpoint 348 N5 theorem fork",
    },
]


VARIATION_TERMS = [
    {
        "term": "S_EH",
        "fields": "metric/coframe g_or_e",
        "variation_piece": "delta_g S_EH -> sqrt(-g)/(2 kappa) (G_munu + Lambda g_munu)",
        "Ward_role": "geometric Bianchi backbone",
        "local_GR_requirement": "survives as the only local exterior metric operator",
        "status": "standard_piece_assumed_as_target_operator",
    },
    {
        "term": "S_matter",
        "fields": "matter psi coupled to one g_or_e",
        "variation_piece": "delta_g S_matter -> -sqrt(-g)/2 T_matter_munu",
        "Ward_role": "universal matter conservation when matter EOM hold",
        "local_GR_requirement": "no independent MTS charge or nonmetric clock/ruler/photon coupling",
        "status": "contract_not_parent_derived",
    },
    {
        "term": "S_X",
        "fields": "memory/load/auxiliary fields X_A",
        "variation_piece": "delta_X S_X and delta_g S_X -> E_X_A plus E_X_metric_munu",
        "Ward_role": "on-shell X removes F_X; off-shell X gives a physical force/residual",
        "local_GR_requirement": "X_A is pure gauge, screened, boundary-only, or source-locked below bounds",
        "status": "open",
    },
    {
        "term": "S_projector",
        "fields": "P_D, relative-chain/cohomology projector, possible constraints",
        "variation_piece": "delta_P S_projector and possible delta_g P_D terms",
        "Ward_role": "hidden projector force must be zero, boundary-only, or retained",
        "local_GR_requirement": "metric-independent local bulk P_D or retained stress with PPN residuals",
        "status": "hard_gate",
    },
    {
        "term": "S_boundary",
        "fields": "boundary/domain data Y_partialD, induced geometry, charges",
        "variation_piece": "delta_boundary S -> flux/current terms plus possible distributional stress",
        "Ward_role": "boundary flux must close conservation or appear as residual",
        "local_GR_requirement": "only conserved monopole mass renormalization may survive locally",
        "status": "open",
    },
    {
        "term": "S_domain",
        "fields": "domain selector chi_D, normal n_mu, coarse-graining scale L_cg",
        "variation_piece": "delta_domain S -> F_domain and preferred-frame/location terms",
        "Ward_role": "fixed external domain data would break diffeomorphism covariance",
        "local_GR_requirement": "domain data must be covariant, dynamical, pure gauge, or locally silent",
        "status": "open",
    },
]


WARD_IDENTITY_STEPS = [
    {
        "step": 1,
        "name": "total_parent_variation",
        "equation": "delta S_parent = delta_g S + delta_psi S + delta_X S + delta_P S + delta_boundary S + delta_domain S",
        "meaning": "all terms that can carry local force are explicitly present",
        "status": "written_as_contract",
    },
    {
        "step": 2,
        "name": "diffeomorphism_variation",
        "equation": "delta_xi g_munu = 2 nabla_(mu xi_nu); delta_xi Phi = L_xi Phi for every parent field Phi",
        "meaning": "no field is allowed to stay fixed if it transforms under spacetime diffeomorphisms",
        "status": "required",
    },
    {
        "step": 3,
        "name": "integrate_by_parts",
        "equation": "0 = integral sqrt(-g) xi_nu I^nu + boundary",
        "meaning": "diffeomorphism invariance gives a Noether/Ward identity, not an optional bookkeeping rule",
        "status": "structural_pass",
    },
    {
        "step": 4,
        "name": "define_auxiliary_force_ledger",
        "equation": "I^nu = nabla_mu(T_matter^munu + kappa^-1 E_MTS^munu) + F_X^nu + F_P^nu + F_boundary^nu + F_domain^nu",
        "meaning": "unowned projector/boundary/domain pieces become explicit force terms",
        "status": "main_result",
    },
    {
        "step": 5,
        "name": "on_shell_reduction",
        "equation": "F_X^nu = F_P^nu = F_boundary^nu = F_domain^nu = 0 => nabla_mu(T_matter^munu + kappa^-1 E_MTS^munu)=0",
        "meaning": "ordinary conservation follows only after every auxiliary sector is varied/on-shell or locally silent",
        "status": "conditional",
    },
    {
        "step": 6,
        "name": "local_GR_reduction_condition",
        "equation": "E_MTS_munu -> 0 plus F_i^nu -> 0/boundary-only through PPN order => local EH exterior",
        "meaning": "Ward closure is necessary but not sufficient for local GR",
        "status": "not_promoted",
    },
]


PROJECTOR_FORKS = [
    {
        "fork": "metric_independent_topological_P_D",
        "delta_g_projector": "zero in local bulk",
        "delta_P_status": "constraint/on-shell relative-chain condition still required",
        "Ward_result": "F_P_bulk = 0 if P_D is diffeo-covariant and constraints are owned",
        "local_GR_status": "best_route",
        "claim_allowed": "conditional N5 support only",
    },
    {
        "fork": "boundary_only_projector_charge",
        "delta_g_projector": "distributional or boundary-supported",
        "delta_P_status": "boundary variation and flux balance required",
        "Ward_result": "F_P_bulk = 0 away from boundary, but F_boundary must close",
        "local_GR_status": "allowed_if_monopole_or_nohair",
        "claim_allowed": "no local GR until boundary no-hair is proven",
    },
    {
        "fork": "metric_dependent_Hodge_or_orthogonal_P_D",
        "delta_g_projector": "generically nonzero",
        "delta_P_status": "must be varied or retained",
        "Ward_result": "T_projector and F_P are physical residuals",
        "local_GR_status": "modified_exterior_unless_cancellation_theorem",
        "claim_allowed": "PPN residuals must be computed",
    },
    {
        "fork": "fixed_external_projector",
        "delta_g_projector": "not varied by fiat",
        "delta_P_status": "not owned",
        "Ward_result": "explicit diffeomorphism-breaking force hidden in F_P",
        "local_GR_status": "forbidden",
        "claim_allowed": "no conservation or GR claim",
    },
    {
        "fork": "retained_bulk_projector_stress",
        "delta_g_projector": "nonzero but included in E_MTS",
        "delta_P_status": "on-shell P equation required",
        "Ward_result": "conservation can be honest, but local residual remains",
        "local_GR_status": "bound_or_demote",
        "claim_allowed": "modified-gravity closure until below source-locked bounds",
    },
]


FORCE_LEDGER = [
    {
        "force": "F_X^nu",
        "origin": "memory/load auxiliary equations not on-shell or not screened",
        "zero_condition": "E_X = 0 plus local pure-gauge/screened/static solution",
        "if_nonzero_maps_to": "bulk residual, fifth force, delta_G, radial potential terms",
    },
    {
        "force": "F_P^nu",
        "origin": "projector variation, hidden metric dependence, or non-covariant projector selection",
        "zero_condition": "metric-independent diffeo-covariant P_D with owned constraints, or retained conserved stress",
        "if_nonzero_maps_to": "anisotropic stress, gamma-1, preferred-frame residuals, conservation failure",
    },
    {
        "force": "F_boundary^nu",
        "origin": "boundary charges, flux through partial D, induced-metric variation",
        "zero_condition": "conserved monopole only, no trace-free/vector/clock/WEP boundary hair",
        "if_nonzero_maps_to": "B_tr_rad, B_TF, B_0i, clock/WEP residuals",
    },
    {
        "force": "F_domain^nu",
        "origin": "domain selector, coarse-graining scale, local normal/frame data",
        "zero_condition": "domain variables are covariant/dynamical or locally constant with no preferred frame",
        "if_nonzero_maps_to": "alpha1, alpha2, xi, preferred-location anisotropy",
    },
    {
        "force": "F_matter_nonmetric^nu",
        "origin": "matter/clocks/rulers/photons do not all couple to one metric/coframe",
        "zero_condition": "universal metric coupling and no species-dependent MTS charge",
        "if_nonzero_maps_to": "WEP, redshift, nonmetric light/ruler residuals",
    },
]


THEOREM_STATUS = [
    {
        "claim": "Ward identity with explicit force ledger",
        "status": "structural_pass",
        "evidence": "diffeomorphism variation requires every unowned sector to appear as F_X/F_P/F_boundary/F_domain",
        "limitation": "formal signs/coefficient normalizations still require a fully specified parent Lagrangian",
    },
    {
        "claim": "projector stress cannot be silently dropped",
        "status": "pass",
        "evidence": "fixed or metric-dependent projector appears as F_P or retained E_MTS stress",
        "limitation": "does not choose the final projector mechanism",
    },
    {
        "claim": "N5 locally safe under topological P_D",
        "status": "conditional_pass",
        "evidence": "if P_D is metric-independent, diffeo-covariant, and constraint-owned, F_P_bulk and T_P_bulk vanish",
        "limitation": "parent derivation of P_D and boundary closure remain open",
    },
    {
        "claim": "local GR follows",
        "status": "fail_not_proven",
        "evidence": "Ward closure is necessary but E_MTS and no-hair are not yet derived",
        "limitation": "must still prove local no-hair/EH exterior and compute residuals",
    },
    {
        "claim": "source-locked PPN runner can be meaningful",
        "status": "conditional_ready_after_equations",
        "evidence": "force ledger identifies residual sectors to feed into checkpoint 354 bounds",
        "limitation": "do not run as proof until residual coefficients/equations are specified",
    },
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "turn F_X/F_P/F_boundary/F_domain into local residual amplitudes with explicit zero/boundary/retained options",
        "pass_condition": "each force either vanishes by mechanism, is boundary-only with no PPN support, or is carried into the residual vector",
    },
    {
        "priority": 2,
        "target": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "task": "derive the metric-only EH exterior once Ward/no-hair conditions are imposed",
        "pass_condition": "no extra local propagating scalar/vector/tensor mode remains through weak-field order",
    },
    {
        "priority": 3,
        "target": "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md",
        "task": "use checkpoint 354 target scales only after residual coefficients exist",
        "pass_condition": "gamma, beta, WEP, clock, and quarantined sectors are either below bounds or explicitly fail",
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
    hard_fail_claims = [row for row in THEOREM_STATUS if row["claim"] == "local GR follows" and row["status"] != "pass"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing else "fail",
            "evidence": "all cited source files exist" if not missing else "; ".join(missing),
        },
        {
            "gate": "all_variation_terms_exposed",
            "status": "pass",
            "evidence": f"{len(VARIATION_TERMS)} parent action sectors listed with variation roles",
        },
        {
            "gate": "Ward_force_ledger_written",
            "status": "pass",
            "evidence": "F_X, F_P, F_boundary, F_domain, and nonmetric matter force channels are explicit",
        },
        {
            "gate": "projector_fork_no_cheat",
            "status": "pass",
            "evidence": "fixed external projector and dropped stress route are forbidden",
        },
        {
            "gate": "N5_promoted",
            "status": "fail",
            "evidence": "topological P_D remains conditional; parent derivation and boundary closure are open",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": hard_fail_claims[0]["evidence"] if hard_fail_claims else "no local GR theorem claimed",
        },
        {
            "gate": "PPN_pass_claimed",
            "status": "fail",
            "evidence": "source-locked runner is deferred until residual coefficients are derived",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "local_GR_promoted": False,
            "PPN_pass_claimed": False,
            "N5_closed": "conditional_only",
            "main_result": "conservation now reads Ward divergence plus explicit projector/boundary/domain force ledger, not assumed zero",
            "next_target": NEXT_TARGET,
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
        "parent_variation_terms.csv": VARIATION_TERMS,
        "Ward_identity_steps.csv": WARD_IDENTITY_STEPS,
        "projector_variation_forks.csv": PROJECTOR_FORKS,
        "force_ledger.csv": FORCE_LEDGER,
        "theorem_status.csv": THEOREM_STATUS,
        "next_queue.csv": NEXT_QUEUE,
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
        "variation_terms": len(VARIATION_TERMS),
        "projector_forks": len(PROJECTOR_FORKS),
        "force_channels": len(FORCE_LEDGER),
        "local_GR_promoted": False,
        "PPN_pass_claimed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text("done\n", encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
