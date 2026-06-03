from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "WEP-species-symmetry-common-F-parent-selector-attempt"
STATUS = "common_F_species_blind_geometry_theorem_conditional_parent_selector_not_derived_eta_WEP_still_active"
CLAIM_CEILING = "common_F_selector_attempt_only_no_WEP_clock_PPN_fifth_force_EH_or_local_GR_pass"
NEXT_TARGET = "389-identity-coframe-parent-selection-principle.md"


SOURCE_DOCS = [
    {
        "path": "360-universal-matter-coupling-theorem-attempt.md",
        "role": "universal matter action and forbidden direct MTS matter vertices",
    },
    {
        "path": "366-representative-invariant-matter-action-for-lifted-C.md",
        "role": "representative invariance kills representative vertices but not species functions",
    },
    {
        "path": "371-WEP-species-universality-or-active-eta-runner.md",
        "role": "eta_WEP active unless F_A(C_D)=F(C_D) is derived",
    },
    {
        "path": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "one observed coframe/common-F remains WEP closure",
    },
    {
        "path": "383-local-bound-runner-v2-from-retained-residuals.md",
        "role": "runner v2 states and eta budget policy",
    },
    {
        "path": "385-observed-coframe-selector-pullback-cancellation-theorem.md",
        "role": "coframe pullback cancellation routes and species symmetry condition",
    },
    {
        "path": "386-local-bound-runner-v2-smoke-matrix.md",
        "role": "eta_WEP suppression budget and fair baseline smoke matrix",
    },
    {
        "path": "387-identity-coframe-or-class-metric-fork.md",
        "role": "identity coframe versus class-metric fork and next common-F target",
    },
    {
        "path": "runs/20260602-014500-local-bound-runner-v2-smoke-matrix/results/suppression_budget_summary.csv",
        "role": "machine-readable eta_WEP suppression budget",
    },
]


THEOREM_ATTEMPTS = [
    {
        "attempt": "diffeomorphism_local_Lorentz_only",
        "premise": "matter actions are diffeomorphism and local-Lorentz invariant",
        "result": "permits species-dependent scalar functions F_A(C_D)",
        "verdict": "fail",
        "why": "spacetime covariance constrains index structure, not species labels",
    },
    {
        "attempt": "representative_invariance_only",
        "premise": "matter cannot depend on B_perp, b_2, scalar Cperp, or representative data",
        "result": "permits F_A(C_D) because C_D is class-invariant",
        "verdict": "fail_for_common_F",
        "why": "quotienting representative data does not quotient species labels",
    },
    {
        "attempt": "full_species_permutation_symmetry",
        "premise": "all matter species are exactly interchangeable",
        "result": "would force common F and also overconstrain masses/charges/representations",
        "verdict": "too_strong_unphysical_as_stated",
        "why": "species differ by internal representations and constants",
    },
    {
        "attempt": "species_blind_geometry_functor",
        "premise": "the parent matter functor lets species labels enter only internal representations/constants, not the geometry map",
        "result": "ehat_A=ehat and F_A(C_D)=F(C_D) for all species",
        "verdict": "conditional_theorem",
        "why": "there is one geometric argument shared by every matter action",
    },
    {
        "attempt": "identity_coframe_selection",
        "premise": "the parent local matter functor selects ehat=e and constants independent of C_D",
        "result": "F_A=0 for all species and Pi_I^matter=0 for nonmetric selector variables",
        "verdict": "strongest_conditional_route",
        "why": "removes class-metric pullback rather than only making it common",
    },
    {
        "attempt": "naturalness_or_smallness",
        "premise": "species functions are expected small or aesthetically disfavoured",
        "result": "does not force Delta F_AB=0",
        "verdict": "fail_as_derivation",
        "why": "eta_WEP requires theorem-zero or source-locked coefficient, not taste",
    },
]


SPECIES_BLIND_FUNCTOR_CONTRACT = [
    {
        "contract_item": "single_geometry_argument",
        "mathematical_statement": "S_matter = sum_A S_A[Psi_A, ehat, omega[ehat], theta_A]",
        "what_it_forbids": "ehat_A and ghat_A species-labelled geometry maps",
        "status": "conditional theorem premise",
    },
    {
        "contract_item": "species_labels_internal_only",
        "mathematical_statement": "theta_A may contain spin, representation, mass, charge constants, but not class functions theta_A(C_D)",
        "what_it_forbids": "m_A(C_D), alpha_A(C_D), q_A(C_D), F_A(C_D)",
        "status": "not parent-derived",
    },
    {
        "contract_item": "class_sector_no_species_spurion",
        "mathematical_statement": "delta S_parent / delta sigma_A = 0 because no species spurion sigma_A couples to C_D",
        "what_it_forbids": "lambda_A f(C_D) O_A and species-specific class charge",
        "status": "required selection rule",
    },
    {
        "contract_item": "common_geometry_map",
        "mathematical_statement": "ehat = ehat(e, C_D, P_D, boundary, bulk, ...), independent of A",
        "what_it_forbids": "partial_A ehat_A or Delta F_AB",
        "status": "conditional common-F result",
    },
    {
        "contract_item": "identity_preference_for_local_GR",
        "mathematical_statement": "local branch sets ehat=e for matter, or proves class pullback is silent/owned",
        "what_it_forbids": "unowned Pi_I^matter",
        "status": "next parent-selection target",
    },
]


NO_GO_RESULTS = [
    {
        "no_go": "covariance_does_not_imply_WEP",
        "statement": "S_A[psi_A, exp(F_A(C_D))g] is covariant for every A",
        "consequence": "diffeomorphism invariance alone cannot derive common F",
    },
    {
        "no_go": "representative_invariance_does_not_remove_species_spurions",
        "statement": "F_A(C_D) is invariant under representative shifts because C_D is invariant",
        "consequence": "lifted-C quotient symmetry does not close eta_WEP",
    },
    {
        "no_go": "full_species_symmetry_is_not_the_right_symmetry",
        "statement": "exchanging all species would also erase physical differences in mass, charge, and representation",
        "consequence": "the needed symmetry is species-blind geometry, not full identity of species",
    },
    {
        "no_go": "common_F_does_not_solve_common_mode",
        "statement": "F_A=F kills species split but leaves common T partial_C F pullback",
        "consequence": "clock/gamma/fifth-force/Gdot rows remain unless local silence/source-normalization/counterstress is derived",
    },
    {
        "no_go": "small_species_functions_are_not_zero",
        "statement": "Delta F_AB can be tiny but eta_WEP budget is 2.8e-15",
        "consequence": "smallness must be sourced, fitted, or theorem-forbidden",
    },
]


ETA_TRANSITION = [
    {
        "eta_term": "Delta F_AB = F_A(C_D)-F_B(C_D)",
        "if_species_blind_functor_parent_derived": "derived_zero",
        "current_status": "conditional_zero_only",
        "budget_if_not_zero": "2.8e-15 total eta_WEP scale",
    },
    {
        "eta_term": "Delta m_A(C_D)",
        "if_species_blind_functor_parent_derived": "derived_zero if masses are constants theta_A independent of C_D",
        "current_status": "conditional_zero_only",
        "budget_if_not_zero": "shares eta_WEP and composition budget",
    },
    {
        "eta_term": "Delta alpha_A(C_D)",
        "if_species_blind_functor_parent_derived": "derived_zero if EM/clock constants are class-independent",
        "current_status": "conditional_zero_only",
        "budget_if_not_zero": "clock plus WEP/composition budget",
    },
    {
        "eta_term": "q_A class/bulk/source charge",
        "if_species_blind_functor_parent_derived": "derived_zero if no species class spurion exists",
        "current_status": "conditional_zero_only",
        "budget_if_not_zero": "composition fifth-force and eta rows",
    },
    {
        "eta_term": "representative leakage eps_rep",
        "if_species_blind_functor_parent_derived": "independent lifted-C theorem handles representative directions",
        "current_status": "conditional gauge zero",
        "budget_if_not_zero": "eta/clock/gamma leakage rows",
    },
]


BRANCH_DECISION = [
    {
        "branch": "identity_metric_coframe",
        "common_F_status": "F_A=0 for all species if parent-selected",
        "WEP_status": "best local-GR route, still not parent-derived",
        "next_action": "derive identity coframe selection principle",
    },
    {
        "branch": "universal_class_metric",
        "common_F_status": "conditional species-blind functor gives F_A=F",
        "WEP_status": "direct species split can be killed, common-mode pullback remains",
        "next_action": "derive source-normalized/local-silent common mode",
    },
    {
        "branch": "species_class_metric",
        "common_F_status": "not allowed for local-GR route unless common-F theorem is supplied",
        "WEP_status": "eta_WEP active",
        "next_action": "demote to active residual branch",
    },
    {
        "branch": "counterstress_class_pullback",
        "common_F_status": "may own rather than kill pullback",
        "WEP_status": "modified-gravity fallback with source budgets",
        "next_action": "write no-hair/source-budget contract if retained",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "A narrow common-F theorem can be written: if the parent matter sector is a species-blind geometry functor, species labels enter only internal representation/constants and no species class spurions exist, then all species share one ehat and F_A(C_D)=F(C_D). But those premises are not yet derived from the MTS parent action. Therefore eta_WEP remains active/conditional, and the cleanest local-GR route remains identity coframe selection.",
        "common_F_theorem_status": "conditional_not_parent_derived",
        "eta_WEP_status": "active_until_species_blind_geometry_or_identity_coframe_is_parent_derived",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "attempt to derive identity coframe selection from the parent local action/equivalence-principle contract",
        "pass_condition": "ehat=e becomes a parent theorem or remains labelled local WEP closure",
    },
    {
        "priority": 2,
        "target": "390-class-metric-counterstress-nohair-contract.md",
        "task": "if class metric is retained, write the exact no-hair/source-budget contract for common-mode pullback stress",
        "pass_condition": "counterstress is no-hair, source-budgeted, or demoted",
    },
    {
        "priority": 3,
        "target": "391-local-GR-stack-after-identity-coframe.md",
        "task": "after WEP pullback handling, roll forward to EH/operator/source-normalization debts",
        "pass_condition": "remaining local-GR gates are listed without matter-pullback ambiguity",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "theorem_attempts_written",
            "status": "pass",
            "evidence": f"{len(THEOREM_ATTEMPTS)} common-F routes audited",
        },
        {
            "gate": "species_blind_geometry_functor_theorem",
            "status": "conditional_pass",
            "evidence": "common F follows if species labels are internal-only and geometry map is species-blind",
        },
        {
            "gate": "species_blind_functor_parent_derived",
            "status": "fail",
            "evidence": "no parent action principle yet forbids species class spurions",
        },
        {
            "gate": "full_species_symmetry_rejected",
            "status": "pass",
            "evidence": "the required symmetry is geometry universality, not identical species",
        },
        {
            "gate": "eta_WEP_resolved",
            "status": "fail",
            "evidence": "common-F theorem is conditional and eta remains active without parent selector",
        },
        {
            "gate": "common_mode_pullback_resolved",
            "status": "fail",
            "evidence": "even common F leaves T partial_C F unless identity/source-normalization/no-hair is derived",
        },
        {
            "gate": "WEP_PPN_or_local_GR_promoted",
            "status": "fail",
            "evidence": "no row moves to derived_zero without parent theorem",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "theorem_attempts.csv", THEOREM_ATTEMPTS)
    write_csv(results_dir / "species_blind_functor_contract.csv", SPECIES_BLIND_FUNCTOR_CONTRACT)
    write_csv(results_dir / "no_go_results.csv", NO_GO_RESULTS)
    write_csv(results_dir / "eta_transition.csv", ETA_TRANSITION)
    write_csv(results_dir / "branch_decision.csv", BRANCH_DECISION)
    write_csv(results_dir / "gate_results.csv", gate_rows(source_rows))
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "theorem_attempts": len(THEOREM_ATTEMPTS),
        "common_F_theorem_conditional": True,
        "species_blind_functor_parent_derived": False,
        "eta_WEP_resolved": False,
        "common_mode_pullback_resolved": False,
        "derived_local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 388 WEP species symmetry/common-F selector artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
