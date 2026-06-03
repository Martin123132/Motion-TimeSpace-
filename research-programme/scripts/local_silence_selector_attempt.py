from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-silence-selector-attempt"
STATUS = "local_silence_exact_if_boundary_bath_and_relative_class_vanish_but_selector_not_parent_derived"
CLAIM_CEILING = "conditional_local_silence_sufficient_conditions_no_local_GR_promotion"


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
        (ROOT / "280-local-branch-status-ledger-and-empirical-closure-pivot.md", "local branch conditional/proxy status"),
        (ROOT / "287-boundary-current-charge-owner-attempt.md", "relative boundary current and local trivial class blocker"),
        (ROOT / "297-two-over-27-derivation-stack-ledger.md", "2/27 ledger and local silence debt"),
        (ROOT / "298-open-boundary-parent-sector-attempt.md", "open sector with local silence clauses"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def sufficient_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "zero_boundary_bath_spectral_density",
            "mathematical_form": "rho_D(omega)=0 on local bound domains",
            "effect": "Gamma_D=0 and N_D=0",
            "status": "sufficient_if_true",
            "blocker": "boundary-state theorem not derived",
        },
        {
            "condition": "trivial_relative_boundary_class",
            "mathematical_form": "[J_B]_D=0 on local bound domains",
            "effect": "no local relative memory charge for S_src",
            "status": "sufficient_if_true",
            "blocker": "representative/domain class not parent-selected",
        },
        {
            "condition": "zero_or_screened_trace_source",
            "mathematical_form": "Lambda_D ||Tr(P_iso q_r)|| <= epsilon_PPN in local domains",
            "effect": "local PPN residual can be bounded",
            "status": "bound_contract",
            "blocker": "no parent calculation of epsilon_loc yet",
        },
        {
            "condition": "cosmological_open_boundary",
            "mathematical_form": "rho_D(omega)>0 and [J_B]_D nontrivial for FLRW coherent domains",
            "effect": "keeps the cosmological branch active",
            "status": "needed_for_nontrivial_cosmology",
            "blocker": "must not be inserted by hand",
        },
    ]


def selector_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "sigma_from_boundary_spectral_density",
            "definition": "sigma_D = 1 if integral rho_D(omega)domega > 0, else 0",
            "what_it_solves": "turns off Gamma_D and N_D when no open boundary bath exists",
            "failure_or_blocker": "rho_D classification is a boundary-state input unless parent-derived",
            "status": "best_conditional_selector",
        },
        {
            "candidate": "sigma_from_relative_class",
            "definition": "sigma_D = 1 if [J_B]_D is nontrivial, else 0",
            "what_it_solves": "turns off trace source for local trivial classes",
            "failure_or_blocker": "current work has not proved local triviality from parent variables",
            "status": "conditional_contract",
        },
        {
            "candidate": "sigma_from_product",
            "definition": "sigma_D = Theta(rho_D) * Theta(||[J_B]_D||)",
            "what_it_solves": "requires both open bath and nontrivial relative charge",
            "failure_or_blocker": "strongest safety filter but both factors are currently theorem targets",
            "status": "recommended_closure_until_derived",
        },
        {
            "candidate": "sigma_from_local_curvature_scalar",
            "definition": "sigma_D=f(R,K,rho_local,...)",
            "what_it_solves": "would be local and covariant if it worked",
            "failure_or_blocker": "risks activating in ordinary local gravitating systems and is not tied to open boundary bath",
            "status": "rejected_for_now",
        },
        {
            "candidate": "constant_small_sigma",
            "definition": "sigma_D=epsilon everywhere",
            "what_it_solves": "could numerically evade local bounds if tiny",
            "failure_or_blocker": "turns into fitted screening parameter and weakens field-theory claim",
            "status": "rejected_as_fundamental_route",
        },
    ]


def exact_silence_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "open_dissipation",
            "formula": "Gamma_D = sigma_D Gamma_open",
            "if_sigma_local_zero": "Gamma_D=0 locally",
            "consequence": "no local irreversible axis-to-trace relaxation from the open sector",
            "status": "exact_conditional",
        },
        {
            "step": "open_noise",
            "formula": "N_D = sigma_D N_open",
            "if_sigma_local_zero": "N_D=0 locally",
            "consequence": "no local open-boundary stochastic source",
            "status": "exact_conditional",
        },
        {
            "step": "trace_source",
            "formula": "Lambda_D = sigma_D Lambda_open or Lambda_D[J_B]_D",
            "if_sigma_local_zero": "Lambda_D=0 locally",
            "consequence": "T_mem local source vanishes in this sector",
            "status": "exact_conditional",
        },
        {
            "step": "PPN_residual_vector",
            "formula": "delta_PPN proportional to epsilon_loc = |Lambda_D Tr(P_iso q_r)|",
            "if_sigma_local_zero": "epsilon_loc=0",
            "consequence": "open-sector PPN residual is zero at this effective level",
            "status": "conditional_bound_not_full_GR_proof",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "open sector alone derives local silence",
            "result": "fail",
            "reason": "S_open can be written for any domain unless domain/boundary state data select sigma_D",
            "consequence": "local silence is not automatic",
        },
        {
            "claim": "relative class alone is enough",
            "result": "fail_as_full_derivation",
            "reason": "local trivial class has been assumed/targeted but not parent-selected",
            "consequence": "needs representative/domain theorem",
        },
        {
            "claim": "boundary bath absence alone is enough",
            "result": "partial",
            "reason": "kills Gamma_D and N_D but not necessarily Lambda_D unless source also depends on bath or [J_B]",
            "consequence": "must tie trace source to same selector",
        },
        {
            "claim": "local curvature scalar selector is safe",
            "result": "rejected_for_now",
            "reason": "ordinary local systems can have curvature/density and would accidentally activate the branch",
            "consequence": "selector should be boundary/topological, not simple local curvature",
        },
    ]


def ppn_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "quantity": "epsilon_loc",
            "definition": "|sigma_D Lambda_open Tr(P_iso q_r)|",
            "acceptance_condition": "epsilon_loc <= epsilon_PPN for the chosen official local-bound manifest",
            "current_status": "symbolic_contract_only",
        },
        {
            "quantity": "delta_gamma_PPN",
            "definition": "C_gamma * epsilon_loc + higher_order_terms",
            "acceptance_condition": "must be below official gamma-bound in local systems",
            "current_status": "coefficient_not_derived",
        },
        {
            "quantity": "delta_beta_PPN",
            "definition": "C_beta * epsilon_loc + higher_order_terms",
            "acceptance_condition": "must be below official beta-bound in local systems",
            "current_status": "coefficient_not_derived",
        },
        {
            "quantity": "fifth_force_residual",
            "definition": "grad(Lambda_D Tr(P_iso q_r))",
            "acceptance_condition": "zero if sigma_D=0; otherwise must be bounded",
            "current_status": "zero_only_under_selector",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    source_missing = [source for source in source_register_rows() if source["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all cited checkpoints exist" if not source_missing else ";".join(source["source"] for source in source_missing),
            "claim_effect": "attempt traceable",
        },
        {
            "gate": "exact_silence_if_selector_zero",
            "status": "pass",
            "evidence": "Gamma_D=N_D=Lambda_D=0 locally if sigma_D=0",
            "claim_effect": "local silence has a mathematically exact sufficient condition",
        },
        {
            "gate": "boundary_bath_selector_defined",
            "status": "conditional_pass",
            "evidence": "sigma_D can be tied to boundary spectral density rho_D and relative class [J_B]_D",
            "claim_effect": "best local selector target identified",
        },
        {
            "gate": "selector_parent_derived",
            "status": "fail",
            "evidence": "no parent theorem proves rho_D=0 and [J_B]=0 in local bound domains",
            "claim_effect": "local silence not promoted",
        },
        {
            "gate": "PPN_residual_bounded",
            "status": "fail",
            "evidence": "only symbolic epsilon_loc contract written; no official bound run or coefficient map",
            "claim_effect": "no local-GR claim",
        },
        {
            "gate": "cosmology_not_silenced",
            "status": "conditional_pass",
            "evidence": "FLRW branch remains active if rho_D>0 and [J_B]_D nontrivial",
            "claim_effect": "selector can in principle separate cosmological and local domains",
        },
        {
            "gate": "B_mem_parent_derived",
            "status": "fail",
            "evidence": "local selector is still conditional and does not derive B3 topology or robust empirical status",
            "claim_effect": "2/27 remains locked closure/theorem target",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "Local silence is exact if the open-sector selector vanishes locally: Gamma_D, N_D, and Lambda_D all "
                "turn off when sigma_D=0, giving zero open-sector local PPN residual at the effective level. The best "
                "non-arbitrary selector is boundary/topological: sigma_D should depend on boundary bath spectral density "
                "and the relative boundary class. But the parent theory has not yet proved rho_D=0 and [J_B]=0 for local "
                "bound domains while keeping the FLRW class active."
            ),
            "next_target": "derive_boundary_state_theorem_or_build_local_bound_runner_for_epsilon_loc",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "sufficient_conditions.csv": (
            sufficient_condition_rows(),
            ["condition", "mathematical_form", "effect", "status", "blocker"],
        ),
        "selector_candidates.csv": (
            selector_candidate_rows(),
            ["candidate", "definition", "what_it_solves", "failure_or_blocker", "status"],
        ),
        "exact_silence_chain.csv": (
            exact_silence_chain_rows(),
            ["step", "formula", "if_sigma_local_zero", "consequence", "status"],
        ),
        "no_go_tests.csv": (
            no_go_rows(),
            ["claim", "result", "reason", "consequence"],
        ),
        "ppn_bound_contract.csv": (
            ppn_contract_rows(),
            ["quantity", "definition", "acceptance_condition", "current_status"],
        ),
        "promotion_gates.csv": (
            promotion_gate_rows(),
            ["gate", "status", "evidence", "claim_effect"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "meaning", "next_target"],
        ),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "exact_local_silence_if_selector_zero": True,
        "selector_parent_derived_now": False,
        "PPN_bound_verified_now": False,
        "B_mem_parent_derived_now": False,
        "next_target": "derive_boundary_state_theorem_or_build_local_bound_runner_for_epsilon_loc",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local silence selector derivation attempt.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
