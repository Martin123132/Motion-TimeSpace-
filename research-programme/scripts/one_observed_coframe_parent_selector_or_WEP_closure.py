from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "one-observed-coframe-parent-selector-or-WEP-closure"
STATUS = "one_observed_coframe_common_F_not_parent_derived_WEP_closure_axiom_required_eta_active"
CLAIM_CEILING = "WEP_closure_axiom_and_selector_audit_only_no_WEP_clock_PPN_EH_or_local_GR_pass"
NEXT_TARGET = "374-fifth-force-preferred-frame-source-lock-manifest.md"


SOURCE_DOCS = [
    {
        "path": "360-universal-matter-coupling-theorem-attempt.md",
        "role": "conditional one-observed-coframe theorem and no-direct-MTS-matter-argument contract",
    },
    {
        "path": "366-representative-invariant-matter-action-for-lifted-C.md",
        "role": "representative invariance kills representative data but permits species-specific F_A(C_D)",
    },
    {
        "path": "371-WEP-species-universality-or-active-eta-runner.md",
        "role": "eta_WEP remains active because species universality is not parent-derived",
    },
    {
        "path": "372-local-phiC-zero-theorem-or-gradient-bound.md",
        "role": "local common-mode phi_C silence is conditional and does not solve species universality",
    },
    {
        "path": "368-common-mode-class-metric-clock-PPN-residual-gate.md",
        "role": "common-mode class metric residuals and local PPN guardrails",
    },
    {
        "path": "369-source-locked-closure-branch-local-bound-runner.md",
        "role": "source-locked closure runner retaining eta_WEP and quarantined fifth-force/preferred-frame rows",
    },
    {
        "path": "10-observer-map-symplectic-contract.md",
        "role": "earlier observer coframe contract requiring universal matter coupling for PPN completion",
    },
    {
        "path": "14-closure-deviation-PPN-sensitivity.md",
        "role": "earlier epsilon_matter/WEP leakage sensitivity context",
    },
]


SELECTOR_CANDIDATES = [
    {
        "candidate": "diffeomorphism_invariance",
        "candidate_statement": "all matter actions are scalar functionals on the same manifold",
        "does_it_select_one_coframe": "no",
        "why": "covariance permits several species metrics or species-specific functions F_A(C_D)",
        "status": "insufficient",
    },
    {
        "candidate": "representative_invariance",
        "candidate_statement": "matter ignores B_perp, b2, scalar Cperp, and local representative data",
        "does_it_select_one_coframe": "no",
        "why": "F_A(C_D) is representative-invariant for every species A",
        "status": "conditional_progress_but_not_WEP",
    },
    {
        "candidate": "common_mode_local_phiC_silence",
        "candidate_statement": "stationary local domains force grad phi_C=0 inside the local-trivial-class branch",
        "does_it_select_one_coframe": "no",
        "why": "it can remove common-mode local gradients but cannot prove F_A=F_B or constant independence",
        "status": "orthogonal_to_species_universality",
    },
    {
        "candidate": "minimal_metric_coupling_principle",
        "candidate_statement": "postulate one observed coframe ehat for all matter, clocks, photons, and rulers",
        "does_it_select_one_coframe": "yes_if_postulated",
        "why": "this is exactly the safe WEP contract but it is an external closure unless parent-owned",
        "status": "closure_axiom",
    },
    {
        "candidate": "internal_species_symmetry",
        "candidate_statement": "a parent symmetry forbids all species labels in class-response functions",
        "does_it_select_one_coframe": "possible",
        "why": "no such symmetry is currently present in the corpus branch being tested",
        "status": "future_theorem_target",
    },
    {
        "candidate": "renormalization_naturalness",
        "candidate_statement": "all allowed species couplings are expected unless symmetry-forbidden",
        "does_it_select_one_coframe": "no",
        "why": "naturalness strengthens the need for a symmetry; it does not supply one",
        "status": "pressure_against_overclaim",
    },
]


NO_GO_STEPS = [
    {
        "step": 1,
        "statement": "Start with the most general representative-invariant matter branch.",
        "equation": "S_m = sum_A S_A[Psi_A, exp(F_A(C_D)) g, constants_A(C_D)]",
        "status": "allowed_by_current_symmetries",
    },
    {
        "step": 2,
        "statement": "Apply lifted-C representative invariance.",
        "equation": "delta_B S_m = 0 forbids B_perp, b2, Cperp, and local j3 representative vertices",
        "status": "conditional_progress",
    },
    {
        "step": 3,
        "statement": "Notice that the species functions survive that projection.",
        "equation": "delta_B F_A(C_D) = 0 for every A",
        "status": "no_go_core",
    },
    {
        "step": 4,
        "statement": "Common-mode local silence cannot remove species labels.",
        "equation": "grad phi_C = 0 does not imply F_A(C_D)=F_B(C_D)",
        "status": "no_go_support",
    },
    {
        "step": 5,
        "statement": "Therefore one observed coframe is not derived by the current branch.",
        "equation": "ehat_A = ehat for all A remains an extra selector condition",
        "status": "fail_parent_derivation",
    },
    {
        "step": 6,
        "statement": "The safe branch remains valid only as an explicit WEP closure axiom or future parent theorem target.",
        "equation": "S_m = sum_A S_A[Psi_A, ehat, omega[ehat], constants_A]",
        "status": "closure_required",
    },
]


PARENT_ACTION_CONTRACT = [
    {
        "contract_item": "unique_observed_coframe",
        "required_statement": "the parent variational problem selects one ehat^a_mu for all matter observables",
        "mathematical_form": "ehat_A^a_mu = ehat^a_mu for every species A",
        "current_status": "not_parent_derived",
    },
    {
        "contract_item": "no_direct_non_geometric_arguments",
        "required_statement": "matter has no direct dependence on MTS variables at fixed observed coframe",
        "mathematical_form": "delta S_matter / delta Z_I | ehat = 0",
        "current_status": "conditional_theorem_if_contract_assumed",
    },
    {
        "contract_item": "no_species_class_functions",
        "required_statement": "species labels cannot enter class-response functions, masses, or constants",
        "mathematical_form": "F_A(C_D)=F(C_D), m_A not equal m_A(C_D), alpha_A not equal alpha_A(C_D)",
        "current_status": "closure_axiom_required",
    },
    {
        "contract_item": "representative_quotient_only",
        "required_statement": "matter sees only class observables, not representative data",
        "mathematical_form": "S_matter = S_matter[Psi, ehat(C_D,g)]",
        "current_status": "conditional_from_lifted_C_representative_invariance",
    },
    {
        "contract_item": "matter_Ward_identity",
        "required_statement": "ordinary matter is covariantly conserved on the observed geometry when no exchange is derived",
        "mathematical_form": "nabla_hat_mu T_hat^mu_nu = 0",
        "current_status": "conditional_if_single_ehat_action_holds",
    },
    {
        "contract_item": "selector_stress_ownership",
        "required_statement": "any projector/coframe/domain selector stress appears in the parent Ward ledger, not hidden in matter",
        "mathematical_form": "nabla_mu(T_matter + T_MTS + T_selector)^mu_nu = 0",
        "current_status": "open_from_prior_Ward_ledgers",
    },
]


WEP_CLOSURE_AXIOMS = [
    {
        "axiom": "W1_one_observed_coframe",
        "statement": "all matter, photons, clocks, rulers, and lab standards couple to one observed coframe",
        "why_needed": "kills direct metric/composition split",
        "status": "explicit_closure_until_parent_selector_exists",
    },
    {
        "axiom": "W2_common_class_function",
        "statement": "there are no species-dependent functions F_A(C_D)",
        "why_needed": "prevents eta_WEP from class-response differences",
        "status": "explicit_closure_until_species_symmetry_exists",
    },
    {
        "axiom": "W3_constant_independence",
        "statement": "dimensionless matter/EM/clock constants do not depend directly on C_D or MTS representatives",
        "why_needed": "prevents clock/composition residuals outside geometry",
        "status": "explicit_closure_until_unification_of_constants_exists",
    },
    {
        "axiom": "W4_representative_invariance",
        "statement": "B_perp, b2, Cperp, and local j3 representative data are unobservable to matter",
        "why_needed": "prevents direct representative fifth-force/WEP vertices",
        "status": "conditional_theorem_target_not_global_pass",
    },
    {
        "axiom": "W5_local_common_mode_silence_or_bound",
        "statement": "common-mode phi_C is locally theorem-zero or source-bounded",
        "why_needed": "prevents clock/gamma/fifth-force pressure after WEP closure",
        "status": "conditional_or_budget_only",
    },
]


ETA_RESIDUAL_VECTOR = [
    {
        "term": "species_class_metric_split",
        "symbolic_form": "Delta F_AB = F_A(C_D) - F_B(C_D)",
        "current_control": "not parent-derived zero",
        "runner_policy": "eta_WEP remains active",
    },
    {
        "term": "species_mass_or_constant_response",
        "symbolic_form": "Delta m_A(C_D), Delta alpha_A(C_D)",
        "current_control": "forbidden only by closure axiom",
        "runner_policy": "eta_WEP and clock rows remain active",
    },
    {
        "term": "representative_vertex_leakage",
        "symbolic_form": "B_perp O_A, b2 O_A, Cperp O_A",
        "current_control": "conditionally forbidden by representative invariance",
        "runner_policy": "conditional zero if lifted-C symmetry is parent-owned",
    },
    {
        "term": "common_mode_gradient",
        "symbolic_form": "grad phi_C or Delta phi_C / Delta U",
        "current_control": "conditional local zero theorem or fallback bounds",
        "runner_policy": "clock/gamma/fifth-force rows remain conditional or budgeted",
    },
]


PROMOTION_RULES = [
    {
        "promotion": "direct_WEP_vertex_absent",
        "allowed_claim": "conditional theorem",
        "required_evidence": "single ehat action plus no direct MTS matter arguments",
        "current_result": "conditional only",
    },
    {
        "promotion": "one_observed_coframe_parent_derived",
        "allowed_claim": "not allowed",
        "required_evidence": "parent symmetry/equation forcing ehat_A=ehat for all species",
        "current_result": "fail",
    },
    {
        "promotion": "WEP_pass",
        "allowed_claim": "not allowed",
        "required_evidence": "eta_WEP theorem-zero or source-locked empirical bound with all active terms controlled",
        "current_result": "fail",
    },
    {
        "promotion": "clock_PPN_pass",
        "allowed_claim": "not allowed",
        "required_evidence": "WEP closure plus local phi_C/EH/fifth-force/preferred-frame controls",
        "current_result": "fail",
    },
    {
        "promotion": "local_GR_pass",
        "allowed_claim": "not allowed",
        "required_evidence": "WEP, clock, PPN, EH exterior, and conservation gates all pass",
        "current_result": "fail",
    },
]


FAILURE_MODES = [
    {
        "failure": "closure_hidden_as_derivation",
        "meaning": "using one observed coframe while claiming it has been parent-selected",
        "consequence": "false WEP/local-GR promotion",
    },
    {
        "failure": "representative_invariance_overclaim",
        "meaning": "forgetting that representative-invariant F_A(C_D) remains possible",
        "consequence": "eta_WEP is incorrectly switched off",
    },
    {
        "failure": "local_phiC_silence_overclaim",
        "meaning": "using common-mode local silence as if it forced species universality",
        "consequence": "composition residuals are missed",
    },
    {
        "failure": "constant_variation_leakage",
        "meaning": "allowing EM/clock/mass constants to depend directly on class variables",
        "consequence": "clock and WEP channels reopen even with one metric",
    },
    {
        "failure": "selector_stress_unowned",
        "meaning": "coframe/projector selector has hidden stress not in the Ward ledger",
        "consequence": "conservation and PPN claims become unsafe",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The current branch conditionally kills direct WEP/clock vertices if one observed coframe and common F(C_D) are assumed, but no parent selector derives that universality; one observed coframe must remain an explicit WEP closure axiom and eta_WEP stays active.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "source-lock fifth-force, preferred-frame, xi, and residual coframe/vector leakage rows before scoring them",
        "pass_condition": "all local residual rows are either theorem-zero, ready budget rows, or explicitly quarantined",
    },
    {
        "priority": 2,
        "target": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "task": "separate Einstein-Hilbert exterior derivation from residual modified-gravity operator testing",
        "pass_condition": "EH operator is derived or modified-gravity residuals are kept in a bounded ledger",
    },
    {
        "priority": 3,
        "target": "376-parent-species-symmetry-or-WEP-closure-deepening.md",
        "task": "look for a genuine parent symmetry that forbids species-specific class functions",
        "pass_condition": "F_A=F is derived, or the WEP closure axiom is accepted as non-derived structure",
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
            "gate": "single_coframe_contract_imported",
            "status": "conditional_pass",
            "evidence": "checkpoint 360 gives exact direct-vertex kill if one observed coframe is assumed",
        },
        {
            "gate": "representative_vertices_forbidden",
            "status": "conditional_pass",
            "evidence": "lifted-C representative invariance forbids B_perp/b2/Cperp matter vertices if parent-owned",
        },
        {
            "gate": "common_F_parent_derived",
            "status": "fail",
            "evidence": "representative invariance and covariance permit species-specific F_A(C_D)",
        },
        {
            "gate": "one_observed_coframe_parent_selected",
            "status": "fail",
            "evidence": "no parent symmetry/equation forces ehat_A=ehat for all species",
        },
        {
            "gate": "WEP_closure_axiom_written",
            "status": "pass",
            "evidence": "W1-W5 closure axioms separate conditional theorem from non-derived selector",
        },
        {
            "gate": "eta_WEP_switched_off",
            "status": "fail",
            "evidence": "eta_WEP remains active until F_A=F and constants are parent-derived",
        },
        {
            "gate": "WEP_clock_PPN_EH_or_local_GR_promoted",
            "status": "fail",
            "evidence": "no observational or local-GR pass follows from this selector audit",
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
    write_csv(results_dir / "selector_candidates.csv", SELECTOR_CANDIDATES)
    write_csv(results_dir / "no_go_steps.csv", NO_GO_STEPS)
    write_csv(results_dir / "parent_action_contract.csv", PARENT_ACTION_CONTRACT)
    write_csv(results_dir / "WEP_closure_axioms.csv", WEP_CLOSURE_AXIOMS)
    write_csv(results_dir / "eta_residual_vector.csv", ETA_RESIDUAL_VECTOR)
    write_csv(results_dir / "promotion_rules.csv", PROMOTION_RULES)
    write_csv(results_dir / "failure_modes.csv", FAILURE_MODES)
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
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 373 one observed coframe selector or WEP closure artifacts."
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
