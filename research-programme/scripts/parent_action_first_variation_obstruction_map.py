from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "parent-action-first-variation-obstruction-map"
STATUS = "parent_action_first_variation_obstruction_map_written_first_unowned_term_is_observed_coframe_selector_pullback_no_local_GR_promotion"
CLAIM_CEILING = "first_variation_obstruction_map_only_no_WEP_PPN_EH_boundary_bulk_source_or_local_GR_pass"
NEXT_TARGET = "385-observed-coframe-selector-pullback-cancellation-theorem.md"


SOURCE_DOCS = [
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "full parent variation and Ward force ledger",
    },
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "EH sufficiency stack and operator obstruction",
    },
    {
        "path": "360-universal-matter-coupling-theorem-attempt.md",
        "role": "fixed-ehat matter variation and no direct MTS matter vertices",
    },
    {
        "path": "364-lifted-C-sector-form-holonomy-theorem-attempt.md",
        "role": "lifted-C conditional route with parent boundary/domain missing",
    },
    {
        "path": "367-topological-class-selection-or-local-GR-closure-ledger.md",
        "role": "class selection closure status",
    },
    {
        "path": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "one observed coframe/common-F closure and eta residual",
    },
    {
        "path": "379-class-only-boundary-action-noangular-theorem.md",
        "role": "boundary action no-angular conditional theorem and retained coefficients",
    },
    {
        "path": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "bulk-X source-free/mass-gap or force-law contract",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "minimal parent local action contract and residual fallbacks",
    },
    {
        "path": "383-local-bound-runner-v2-from-retained-residuals.md",
        "role": "local-bound runner v2 and top active WEP pressure row",
    },
]


VARIATION_CHAIN = [
    {
        "step": 1,
        "variation": "delta_psi S_parent",
        "formal_result": "matter equations of motion",
        "obstruction_status": "owned_on_matter_shell",
        "comment": "standard matter variation is not the first obstruction",
    },
    {
        "step": 2,
        "variation": "delta_e_or_delta_g S_parent",
        "formal_result": "E_EH + E_MTS_metric = kappa T_hat plus selector/projector/boundary/source stresses",
        "obstruction_status": "requires_EH_operator_and_source_normalization_later",
        "comment": "metric stress is expected, but local GR still needs EH-only exterior",
    },
    {
        "step": 3,
        "variation": "delta_Z S_matter at fixed ehat",
        "formal_result": "delta S_matter / delta Z_I | ehat = 0",
        "obstruction_status": "conditional_pass_if_one_coframe_action_assumed",
        "comment": "direct non-geometric WEP vertices vanish only at fixed observed coframe",
    },
    {
        "step": 4,
        "variation": "total delta_Z S_matter when ehat = ehat(g,C,P_D,X,boundary,domain,...)",
        "formal_result": "(delta S_matter/delta ehat^a_mu) (delta ehat^a_mu/delta Z_I)",
        "obstruction_status": "first_unowned_term",
        "comment": "coframe selector pullback reintroduces matter stress into selector/class/projector equations",
    },
    {
        "step": 5,
        "variation": "delta_Z S_selector + pullback term",
        "formal_result": "E_selector_I + T_hat^{mu nu} partial ghat_munu/partial Z_I = 0",
        "obstruction_status": "requires_parent_selector_or_counterstress",
        "comment": "without a selector theorem, this is a closure/modified-matter-force row",
    },
    {
        "step": 6,
        "variation": "delta_boundary/domain/X/projector after pullback",
        "formal_result": "boundary, domain, projector, and X equations receive possible source terms",
        "obstruction_status": "secondary_obstructions",
        "comment": "these are serious, but the coframe pullback appears first",
    },
]


OBSTRUCTION_CANDIDATES = [
    {
        "rank": 1,
        "obstruction": "observed_coframe_selector_pullback",
        "equation": "Pi_I^matter := (delta S_matter/delta ehat^a_mu)(partial ehat^a_mu/partial Z_I)",
        "why_first": "direct matter vertices vanish only at fixed ehat; parent variation must still vary the selector defining ehat",
        "current_status": "not_owned",
        "residual_if_failed": "eta_WEP; alpha_clock; nonmetric_light; species_charge; phiC_common_mode",
    },
    {
        "rank": 2,
        "obstruction": "EH_operator_selection",
        "equation": "S_ext = S_EH + sum_i c_i O_i + boundary",
        "why_first": "after force closure, non-EH conserved operators can still survive",
        "current_status": "not_parent_derived",
        "residual_if_failed": "gamma; beta; xi; fifth_force; Gdot",
    },
    {
        "rank": 3,
        "obstruction": "source_normalization_pullback",
        "equation": "delta(G_eff M_eff) must be constant universal, not species/range/time dependent",
        "why_first": "Newtonian limit cannot absorb nonconstant source response",
        "current_status": "not_parent_derived",
        "residual_if_failed": "delta_G; Gdot; beta; fifth_force; WEP",
    },
    {
        "rank": 4,
        "obstruction": "class_only_boundary_variation",
        "equation": "delta S_boundary/delta B_TF = delta S_boundary/delta B_0i = 0 and flux owned",
        "why_first": "boundary hair feeds local observables if the action has angular/vector/radial arguments",
        "current_status": "conditional_not_parent_derived",
        "residual_if_failed": "eps_B_TF; eps_B0i; eps_B_rad; eps_B_flux",
    },
    {
        "rank": 5,
        "obstruction": "bulk_X_operator_or_source",
        "equation": "(-Delta+m_X^2)X=0 or (-Delta+m_X^2)X=q_X rho_source",
        "why_first": "bulk X can become fifth-force/scalar hair if not no-hair or source-normalized",
        "current_status": "contract_not_parent_derived",
        "residual_if_failed": "epsilon_bulk; alpha_X(lambda_X); gamma; beta",
    },
]


COFRAME_PULLBACK_TERMS = [
    {
        "term": "universal_common_mode_pullback",
        "schematic_form": "T_hat^{mu nu} partial[exp(F(C_D)) g_munu]/partial C_D",
        "safe_if": "F is common to all species and locally constant/theorem-zero or absorbed only as constant GM calibration",
        "danger_if": "grad F, time drift, or source dependence survives",
        "residual_rows": "alpha_clock; gamma; fifth_force; Gdot",
    },
    {
        "term": "species_class_pullback",
        "schematic_form": "T_A^{mu nu} partial[exp(F_A(C_D)) g_munu]/partial C_D",
        "safe_if": "parent symmetry forces F_A=F for all species",
        "danger_if": "F_A-F_B survives as class response",
        "residual_rows": "eta_WEP; composition_fifth_force",
    },
    {
        "term": "projector_selector_pullback",
        "schematic_form": "T_hat^{mu nu} partial[P_D C]/partial P_D or partial[P_D C]/partial domain",
        "safe_if": "P_D is covariant, metric-independent/topological, and selector stress is owned",
        "danger_if": "metric-dependent or fixed projector stress is dropped",
        "residual_rows": "gamma; xi; alpha1; alpha2; conservation_failure",
    },
    {
        "term": "boundary_coframe_pullback",
        "schematic_form": "T_hat^{mu nu} partial ehat_munu/partial B_partialD",
        "safe_if": "boundary action is class-only and matter sees no boundary marker/vector data",
        "danger_if": "angular/vector/radial boundary data enter observed coframe",
        "residual_rows": "gamma; beta; alpha1; alpha2; xi; WEP_boundary",
    },
    {
        "term": "bulk_X_matter_pullback",
        "schematic_form": "T_hat^{mu nu} partial ehat_munu/partial X or q_test X_mu J_matter^mu",
        "safe_if": "partial ehat/partial X=0 locally or X is pure gauge/no-hair with no test charge",
        "danger_if": "X carries source/test charge or radial profile",
        "residual_rows": "fifth_force; eta_WEP_if_species; gamma; beta",
    },
]


OWNERSHIP_ROUTES = [
    {
        "route": "strict_identity_coframe",
        "condition": "ehat is the fundamental metric/coframe e for all matter and has no dependence on MTS selector variables",
        "would_do": "matter stress goes only into ordinary metric equation",
        "cost": "MTS local effects must enter only through metric operator/source terms, not matter metric selection",
        "status": "clean_but_closure_unless_parent_identity_selector_derived",
    },
    {
        "route": "parent_species_symmetry",
        "condition": "internal symmetry forces ehat_A=ehat and F_A(C_D)=F(C_D)",
        "would_do": "kills species class pullback and WEP composition row",
        "cost": "still needs common-mode local silence/source normalization",
        "status": "future_theorem_target",
    },
    {
        "route": "quotient_gauge_selector",
        "condition": "Cperp/representative changes are exact gauge and matter depends only on quotient class P_D C",
        "would_do": "kills raw Cperp trace source",
        "cost": "does not by itself force species-universal F(C_D)",
        "status": "conditional_support_only",
    },
    {
        "route": "selector_counterstress_Ward_owned",
        "condition": "selector action variation supplies a stress/current whose divergence cancels the pullback",
        "would_do": "keeps conservation honest without pretending pullback is zero",
        "cost": "counterstress must not create PPN/WEP/preferred-frame residuals above budgets",
        "status": "open_modified_gravity_route",
    },
    {
        "route": "closure_axiom",
        "condition": "declare one coframe/common F and local common-mode silence as branch closure",
        "would_do": "allows budget-only tests as labelled closure",
        "cost": "not a parent derivation; no local-GR promotion",
        "status": "allowed_only_if_labelled",
    },
]


RESIDUAL_IMPACT = [
    {
        "residual": "eta_WEP",
        "source_lock": "2.8e-15",
        "pullback_source": "species class pullback or X/test charge species dependence",
        "runner_state": "budget_only_hardest_ready_row",
    },
    {
        "residual": "alpha_clock_redshift",
        "source_lock": "3.1e-5",
        "pullback_source": "clock metric mismatch or common-mode time drift",
        "runner_state": "budget_only",
    },
    {
        "residual": "gamma_minus_1",
        "source_lock": "2.3e-5",
        "pullback_source": "nonmetric light, boundary shear/radial hair, bulk/scalar stress",
        "runner_state": "budget_only",
    },
    {
        "residual": "beta_minus_1",
        "source_lock": "7.8e-5",
        "pullback_source": "radial/nonlinear boundary, source normalization, bulk X",
        "runner_state": "budget_only",
    },
    {
        "residual": "alpha1_alpha2_xi",
        "source_lock": "1.0e-4; 2.0e-9; 4.0e-9",
        "pullback_source": "domain/projector/boundary vector or anisotropic coframe selector",
        "runner_state": "budget_only",
    },
    {
        "residual": "Gdot_over_G",
        "source_lock": "9.6e-15 yr^-1",
        "pullback_source": "time-varying source normalization/common mode",
        "runner_state": "contingent_budget",
    },
    {
        "residual": "delta_G_or_fifth_force",
        "source_lock": "alpha(lambda)",
        "pullback_source": "radial common mode, bulk X, boundary radial hair, source normalization",
        "runner_state": "unscored_parameterized",
    },
]


CONTRACT_UPDATE = [
    {
        "contract_item": "matter_coframe_identity",
        "old_statement": "delta S_matter/delta Z_I at fixed ehat is zero",
        "new_required_statement": "total selector variation also has Pi_I^matter=(delta S_matter/delta ehat)(partial ehat/delta Z_I) zero, pure gauge, universal constant, or Ward-owned",
        "status": "strengthened",
    },
    {
        "contract_item": "one_coframe_selector",
        "old_statement": "one coframe/common F is required",
        "new_required_statement": "parent action must force one coframe/common F and control its pullback in selector equations",
        "status": "first_obstruction_target",
    },
    {
        "contract_item": "runner_v2",
        "old_statement": "eta_WEP is budget-only hardest ready row",
        "new_required_statement": "eta_WEP remains active until coframe pullback is derived zero/owned or explicitly closure-labelled",
        "status": "unchanged_but_better_sourced",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The first variation of the parent local action hits the observed-coframe selector pullback. Direct matter vertices can vanish at fixed ehat, but if ehat is selected from MTS/class/projector/domain fields, total variation produces (delta S_matter/delta ehat)(partial ehat/partial Z). This term is not currently parent-owned and maps first to WEP/clock/nonmetric rows, with eta_WEP the hardest ready row. Local GR is not promoted.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "try to cancel or forbid the observed-coframe selector pullback by identity coframe, species symmetry, quotient gauge, or Ward-owned counterstress",
        "pass_condition": "Pi_I^matter is derived zero, pure gauge, constant universal, or retained with coefficients",
    },
    {
        "priority": 2,
        "target": "386-local-bound-runner-v2-smoke-matrix.md",
        "task": "run a small coefficient sensitivity smoke for the retained pullback-driven residual rows with a GR/null baseline",
        "pass_condition": "budgets populate with no pass claims and eta_WEP pressure remains explicit",
    },
    {
        "priority": 3,
        "target": "387-EH-operator-first-variation-obstruction.md",
        "task": "after coframe pullback, inspect the metric variation for the first non-EH operator obstruction",
        "pass_condition": "non-EH coefficients are derived zero or retained in the operator ledger",
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
            "gate": "first_variation_chain_written",
            "status": "pass",
            "evidence": f"{len(VARIATION_CHAIN)} variation steps mapped",
        },
        {
            "gate": "first_obstruction_identified",
            "status": "pass",
            "evidence": "observed coframe selector pullback is first unowned term",
        },
        {
            "gate": "coframe_pullback_terms_mapped",
            "status": "pass",
            "evidence": f"{len(COFRAME_PULLBACK_TERMS)} pullback term classes mapped",
        },
        {
            "gate": "ownership_routes_written",
            "status": "pass",
            "evidence": f"{len(OWNERSHIP_ROUTES)} possible ownership routes classified",
        },
        {
            "gate": "pullback_obstruction_solved",
            "status": "fail",
            "evidence": "no parent identity coframe/species symmetry/selector counterstress derived",
        },
        {
            "gate": "WEP_or_PPN_pass_claimed",
            "status": "fail",
            "evidence": "eta_WEP and related rows remain active/budget-only",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "first variation obstruction is mapped, not solved",
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
    write_csv(results_dir / "variation_chain.csv", VARIATION_CHAIN)
    write_csv(results_dir / "obstruction_candidates.csv", OBSTRUCTION_CANDIDATES)
    write_csv(results_dir / "coframe_pullback_terms.csv", COFRAME_PULLBACK_TERMS)
    write_csv(results_dir / "ownership_routes.csv", OWNERSHIP_ROUTES)
    write_csv(results_dir / "residual_impact.csv", RESIDUAL_IMPACT)
    write_csv(results_dir / "contract_update.csv", CONTRACT_UPDATE)
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
        "variation_steps": len(VARIATION_CHAIN),
        "first_obstruction": "observed_coframe_selector_pullback",
        "coframe_pullback_terms": len(COFRAME_PULLBACK_TERMS),
        "ownership_routes": len(OWNERSHIP_ROUTES),
        "pullback_obstruction_solved": False,
        "derived_local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 384 parent-action first-variation obstruction-map artifacts."
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
